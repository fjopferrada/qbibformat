#!/usr/bin/python3

import sys
import os
import pexpect
import subprocess
from subprocess import PIPE

def main():

  p = subprocess.Popen(["bibtool", "-R",
                        "--", "select {$key \"%s\"}" % sys.argv[1],
                        "--", "delete.field { abstract }",
                        "--", "delete.field { mynote }",
                        "--", "delete.field { url }",
                        "~/files/mine/text/bibliography/geoscience.bib",
                        "-o", "temp.bib"
                      ])
  p.wait()

  p = subprocess.Popen(["pandoc", "-t", "latex",
                        "--csl", "apa.csl",
                        "--bibliography", "temp.bib"],
                       stdout=PIPE, stdin=PIPE, stderr=PIPE)
  input = "@%s\n" % sys.argv[1]
  outputs = p.communicate(input.encode())
  print(outputs[0].decode())

# To copy rich text to the clipboard:
# echo "to <b>boldly</b> go" | xclip -selection clipboard -t text/html

if __name__=="__main__":
  main()

