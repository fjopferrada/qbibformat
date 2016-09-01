#!/usr/bin/python3

"""
qbibformat: put a formatted BibTeX entry on the clipboard

Requirements: beautiful soup, bibtool, pandoc, xclip.
"""

import sys
import os.path
from subprocess import PIPE, Popen
from bs4 import BeautifulSoup
from tempfile import TemporaryDirectory

### Main configuration options ######################################

BIBFILE = "demo.bib"
STYLE_FILE = "harvard1.csl"

#####################################################################

def extract_and_format(bibfile, key, tempdir):

  tempfile = os.path.join(tempdir, "temp.bib")

  # Extract the desired entry using bibtool and write it to a
  # temporary .bib file. Unwanted fields can also be removed
  # at this stage.
  bibtool = Popen(
    ["bibtool", "-R",
     "--", "select {$key \"%s\"}" % key,
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
                  "--to", "html",
                  "--csl", STYLE_FILE,
                  "--bibliography", tempfile],
                 stdout=PIPE, stdin=PIPE, stderr=PIPE)
  pandoc_output = pandoc.communicate(source.encode())[0]

  return pandoc_output

def main():

  with TemporaryDirectory() as tempdir:
    pandoc_output = extract_and_format(BIBFILE, sys.argv[1], tempdir)

  # Pandoc adds some divs around the citation. We use BeautifulSoup
  # to extract the first <p> element, which contains the bare 
  # citation itself.
  soup = BeautifulSoup(pandoc_output.decode("utf-8"))
  par = soup.find("p")

  # We use xclip to place the HTML fragment on the X clipboard. Note
  # that there is no X clipboard buffer! xclip must remain running to
  # handle the interclient communication when the contents are pasted.
  # The "-loops 1" argument tells it to exit after the first transfer.
  xclip = Popen(["xclip",
                 "-selection", "clipboard",
                 "-loops", "1",
                 "-target", "text/html"],
                stdin=PIPE, stdout=PIPE)
  xclip.communicate(par.encode("utf-8"))
  #xclip.communicate(pandoc_output)

if __name__=="__main__":
  main()
