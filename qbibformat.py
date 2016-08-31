#!/usr/bin/python3

import sys
import os
import pexpect
import subprocess
from subprocess import PIPE, DEVNULL, Popen

def main():

  bibtool = Popen(
    ["bibtool", "-R",
     "--", "select {$key \"%s\"}" % sys.argv[1],
     "--", "delete.field { abstract }",
     "--", "delete.field { mynote }",
     "--", "delete.field { url }",
     "~/files/mine/text/bibliography/geoscience.bib",
     "-o", "temp.bib"
   ], stderr = DEVNULL)
  bibtool.wait()

  source = "@%s\n" % sys.argv[1]

  pandoc = Popen(["pandoc", "-t", "html",
                        "--csl", "apa.csl",
                        "--bibliography", "temp.bib"],
                       stdout=PIPE, stdin=PIPE, stderr=PIPE)

  pandoc_output = pandoc.communicate(source.encode())[0]
  print(pandoc_output.decode())

  xclip = Popen(["xclip",
                 "-selection", "clipboard",
                 "-loops", "1",
                 "-target", "text/html"],
                stdin=PIPE, stdout=PIPE)

  xclip.communicate(pandoc_output)
  # print(outputs[0].decode())

if __name__=="__main__":
  main()

