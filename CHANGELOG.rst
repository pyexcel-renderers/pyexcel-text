Change log
================================================================================

Planned
--------------------------------------------------------------------------------

#. compactibility with pyexcel-io 0.2.0 and pyexcel 0.2.1


0.2.0 - 23.04.2016
--------------------------------------------------------------------------------

It is a complete re-write of the whole extension.

Added
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. html support
#. support pyexcel 0.2.0's generator output
#. pypy and pypy3 in test targets
#. support file stream and dot notation, e.g. pyexcel.Sheet.rst will return rst text representation of it.

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. `#8 <https://github.com/pyexcel/pyexcel-text/issues/8>`_, write_header as an option(False) to disable header writing
#. the json output of multiple sheet book will be sorted by its sheet names.
#. No longer, pyexcel-text is pyexcel-io plugin but pyexcel.sources plugin.

0.1.1 - 30.01.2016
--------------------------------------------------------------------------------

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. `#2 <https://github.com/pyexcel/pyexcel-text/issues/2>`_, fix a typo in setup.py


0.1.0 - 17.01.2016
--------------------------------------------------------------------------------

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. support pyexcel 0.2.0


0.0.3 - 12.06.2015
--------------------------------------------------------------------------------

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. `#1 <https://github.com/pyexcel/pyexcel-text/issues/1>`_, align api interface
    with other pyexcel plugins, e.g. save_as, save_book_as

0.0.2 - 30.11.2014
--------------------------------------------------------------------------------

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. support pyexcel 0.0.9


0.0.` - 20.11.2014
--------------------------------------------------------------------------------

Initial release



