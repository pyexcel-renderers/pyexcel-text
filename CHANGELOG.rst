Change log
================================================================================

0.2.6 - 19.06.2017
--------------------------------------------------------------------------------

Updated:
********************************************************************************

#. Support pyexcel v0.5.0. Plugin interface updated to Renderer
#. removed deprecated save_as and save_to_memory functions


0.2.5 - 28.10.2016
--------------------------------------------------------------------------------

Updated:
********************************************************************************

#. Support pyexcel v0.4.0

0.2.4 - 28.10.2016
--------------------------------------------------------------------------------

Added:
********************************************************************************

#. support pyexcel v0.3.0


0.2.3 - 14.07.2016
--------------------------------------------------------------------------------

Added:
********************************************************************************

#. json format: serialize date and datetime

Updated:
********************************************************************************

#. if a sheet has row_names, its json output become records(a list of dictionary)
   instead of a dictionary of row name vs the rest of row values.

0.2.2 - 01.06.2016
--------------------------------------------------------------------------------

#. quick bug fix, see `issue #27 <https://github.com/pyexcel/pyexcel-text/issues/27>`_

 
0.2.1 - 01.06.2016
--------------------------------------------------------------------------------

#. compactibility with pyexcel-io 0.2.0 and pyexcel 0.2.2


0.2.0 - 23.04.2016
--------------------------------------------------------------------------------

It is a complete re-write of the whole extension.

Added
********************************************************************************

#. html support
#. support pyexcel 0.2.0's generator output
#. pypy and pypy3 in test targets
#. support file stream and dot notation, e.g. pyexcel.Sheet.rst will return rst text representation of it.

Updated
********************************************************************************

#. `#8 <https://github.com/pyexcel/pyexcel-text/issues/8>`_, write_header as an option(False) to disable header writing
#. the json output of multiple sheet book will be sorted by its sheet names.
#. No longer, pyexcel-text is pyexcel-io plugin but pyexcel.sources plugin.

0.1.1 - 30.01.2016
--------------------------------------------------------------------------------

Updated
********************************************************************************

#. `#2 <https://github.com/pyexcel/pyexcel-text/issues/2>`_, fix a typo in setup.py


0.1.0 - 17.01.2016
--------------------------------------------------------------------------------

Updated
********************************************************************************

#. support pyexcel 0.2.0


0.0.3 - 12.06.2015
--------------------------------------------------------------------------------

Updated
********************************************************************************

#. `#1 <https://github.com/pyexcel/pyexcel-text/issues/1>`_, align api interface
    with other pyexcel plugins, e.g. save_as, save_book_as

0.0.2 - 30.11.2014
--------------------------------------------------------------------------------

Updated
********************************************************************************

#. support pyexcel 0.0.9


0.0.` - 20.11.2014
--------------------------------------------------------------------------------

Initial release



