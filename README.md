qbibformat
==========

A utility to turn individual BibTeX entries into formatted rich text
and place them on the X clipboard.

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
style, and copy it to the clipboard. This is what qbibformat does.
The style is defined by a CSL (Citation Style Language) file.

Dependencies
------------

qbibformat requires Python 3 with the Beautiful Soup library, and
the external programs bibtool, pandoc, and xclip. Because qbibformat
uses xclip to put the reference on the clipboard, it will only work
under the X window system.

Configuration
-------------

All configuration is done by editing the script directly. The most
important parameters are the location of the bibliography file and
the location of the CSL file; these are stored in the BIBFILE and
STYLE_FILE variables defined near the start of the script.

Usage
-----

    qbibformat <somebibtexkey> ...

Where the `<somebibtexkey>` arguments are the keys of the items you want
to extract from your .bib file.

Note that the output is sent to the clipboard as HTML, and can only be
pasted into applications that accept HTML (e.g. LibreOffice Writer,
Google Docs). If plain text output is required, the "--target" argument
in qbibformat's call to xclip can easily be changed.

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
