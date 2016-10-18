#!/usr/bin/python3

# qbibformat is Copyright 2016 Pontus Lurcock (pont at talvi dot net)
# and released under the MIT license:

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
qbibformat: put a formatted BibTeX entry on the clipboard

Requirements: beautiful soup, bibtool, pandoc, xclip.
"""

import sys
import os.path
import argparse
from subprocess import PIPE, Popen
from bs4 import BeautifulSoup
from tempfile import TemporaryDirectory
from functools import reduce

### Main configuration options ######################################

BIBFILE = "demo.bib"
STYLE_FILE = "harvard1.csl"

#####################################################################

def extract_and_format(bibfile, keys, tempdir, output_type):

  tempfile = os.path.join(tempdir, "temp.bib")

  # Build the key selection arguments for bibtool.
  sel_args = reduce(
    lambda args, key: args + ["--", "select {$key \"%s\"}" % key],
    keys, [])
  sel_args_flat = []

  # Extract the desired entries using bibtool and write them to a
  # temporary .bib file. Unwanted fields can also be removed
  # at this stage.
  for key in keys:
    bibtool = Popen(
      ["bibtool", "-R"] + sel_args + [
       "--", "delete.field { abstract }",
       "--", "delete.field { mynote }",
       "--", "delete.field { url }",
       bibfile,
       "-o", tempfile,
       "-q" # suppress warnings
     ])
    bibtool.wait()
  
  # Minimal Markdown input for pandoc.
  # Since version 0.4, pandoc-citeproc supports a wildcard nocite.
  source = "---\nnocite: '@*'\n...\n"

  # Run pandoc
  pandoc = Popen(["pandoc",
                  "--wrap", "none",
                  "--to", {"html":"html","text":"plain"}[output_type],
                  "--csl", STYLE_FILE,
                  "--bibliography", tempfile],
                 stdout=PIPE, stdin=PIPE, stderr=PIPE)
  pandoc_output = pandoc.communicate(source.encode())[0]
  return pandoc_output

def main():

  parser = argparse.ArgumentParser(description="Put a formatted bibtex entry on the clipboard.")

  parser.add_argument("bibtex_key", metavar="bibtex-key", type=str, nargs="+",
                      help="keys of bibtex entries to format")
  parser.add_argument("-t", "--output-type", dest="output_type",
                      type=str,
                      choices=["text", "html"], default="html")
  args = parser.parse_args()

  with TemporaryDirectory() as tempdir:
    pandoc_output = extract_and_format(BIBFILE, args.bibtex_key,
                                       tempdir, args.output_type)

  if args.output_type == "text":
    if pandoc_output == "":
      print("No valid items to copy to the clipboard.")
      return
    parstring = pandoc_output
    print(parstring)
  else:
    # Pandoc adds some divs around the citations. We use BeautifulSoup to
    # extract the <p> elements, which contain the bare citations.
    soup = BeautifulSoup(pandoc_output.decode("utf-8"))

    pars = list(map(str, soup.findAll("p")))

    if len(pars) == 0:
      print("No valid items to copy to the clipboard.")
      return

    parstring = reduce(lambda a, b: a + "\n" + b, pars, "").encode("utf-8")

  target_map = {"text": "text/plain;charset=utf-8", "html": "text/html"}

  # We use xclip to place the HTML fragment on the X clipboard. Note
  # that there is no X clipboard buffer! xclip must remain running to
  # handle the interclient communication when the contents are pasted.

  # The "-loops" argument tells how many transfers to carry out before
  # exiting. "-loops 0" will loop infinitely.
  xclip = Popen(["xclip",
                 "-selection", "clipboard",
                 "-loops", "0",
                 "-verbose",
                 "-target", target_map[args.output_type]],
                stdin=PIPE)#, stdout=PIPE)
  xclip.communicate(parstring)

if __name__=="__main__":
  main()
