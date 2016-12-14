qbibformat
==========

A utility to turn individual BibTeX entries into formatted plain text or
HTML and write them to the standard output, a file, or the X clipboard.

Copyright Pontus Lurcock, 2016. Released under the MIT licence.

Introduction
------------

I have a single, large .bib file containing all my bibliographic
references. Sometimes I work on documents which require a list of
references, but aren't amenable to the use of reference management
software -- either because the platform (e.g. Google Docs) doesn't
support it, or because my co-authors aren't comfortable with it.

In such sitations, I frequently want to extract a single entry from my
BibTeX master file, format it according to a specified bibliographic
style, and write it to a file or copy it to the clipboard. This is what
qbibformat does. The style is defined by a CSL (Citation Style Language)
file.

Dependencies
------------

qbibformat requires Python 3 with the Beautiful Soup library, and
the external programs bibtool, pandoc, and xclip. Because qbibformat
uses xclip to put the reference on the clipboard, it will only work
under the X window system.

Usage
-----

    qbibformat [-h] [-t {text,html}] [-o <filename>] [-c] [-q]
	           <bibtex-key> [<bibtex-key> ...]

Where the `<bibtex-key>` arguments are the keys of the items you want
to extract from your .bib file.

By default, the formatted entries are written to the standard output
only.

Options
-------

`-h`, `--help` Display help and exit.

`-b <filename>, --bib-file <filename>` Bibliography file from which
to read entries.

`-s <filename>, --style-file <filename>` CSL file to use when formatting
entries.

`-t <type>`, `--output-type <type>` Set output type for formatted
entries. Allowed values are `text` and `html`.

`-o <filename>`, `--output-file <filename>` Write formatted entries to
the specified file.

`-q`, `--quiet` Do not write formatted entries to standard output.

`-c`, `--clipboard` Copy formatted entries to the X clipboard.

Configuration file
------------------

The `--bib-file` and `--style-file` options can also be specified in a
configuration file called `.qbibformat` in the user's home directory.
An example configuration file follows:

    [DEFAULT]
    StyleFile = harvard1.csl
    BibFile = demo.bib

Examples
--------

    qbibformat --output-type text smith2000weasels

Take the entry `smith2000weasels` from the configured bibliography file,
format it as plain text according to the configured style file, and
write it to the standard output.

    qbibformat --clipboard --quiet smith2000weasels blazek2001badgers

Take the entries `smith2000weasels`and `blazek2001badgers` from the
configured bibliography file, format them as HTML according to the
configured style file, and put them on the clipboard.

    qbibformat --bib-file demo.bib --style-file harvard1.csl blazek2001badgers

Take the entry `blazek2001badgers` from `demo.bib`, format it as HTML
according to `harvard1.csl`, and write it to the standard output.

Notes on the X clipboard
------------------------

Note that if the output is sent to the clipboard as HTML, it can only
be pasted into applications that accept HTML (e.g. LibreOffice Writer,
Google Docs).

Because of the way the X clipboard works, xclip -- and therefore
qbibformat -- must keep running in order to supply the clipboard
contents when they are pasted. Once the clipboard has been pasted,
qbibformat can be terminated with ctrl-C at the command line, or by
putting something else on the clipboard.

Demo
----

qbibformat is supplied with a sample bib file `demo.bib`, a CSL file
`harvard1.csl`, and a demo script `demo.sh`. Run the script to
demonstrate qbibformat's functionality.
