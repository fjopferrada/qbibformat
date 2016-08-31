#!/usr/bin/python3

import sys
from subprocess import PIPE, DEVNULL, Popen
from bs4 import BeautifulSoup

def main():

  # Extract the desired entry using bibtool.
  bibtool = Popen(
    ["bibtool", "-R",
     "--", "select {$key \"%s\"}" % sys.argv[1],
     "--", "delete.field { abstract }",
     "--", "delete.field { mynote }",
     "--", "delete.field { url }",
     "~/files/mine/text/bibliography/geoscience.bib",
     "-o", "temp.bib",
     "-q" # suppress warnings
   ])
  bibtool.wait()

  # Minimal Markdown input for pandoc.
  # Since version 0.4, pandoc-citeproc supports a wildcard nocite.
  source = "---\nnocite: '@*'\n...\n"

  # Run pandoc
  pandoc = Popen(["pandoc",
                  "--to", "html",
                  "--csl", "apa.csl",
                  "--bibliography", "temp.bib"],
                 stdout=PIPE, stdin=PIPE, stderr=PIPE)
  pandoc_output = pandoc.communicate(source.encode())[0]

  # Pandoc adds some divs around the citation. We use BeautifulSoup
  # to extract the first <p> element, which contains the bare 
  # citation itself.
  soup = BeautifulSoup(pandoc_output)
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

if __name__=="__main__":
  main()
