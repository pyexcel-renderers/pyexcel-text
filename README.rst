=============================================================
pyexcel-text - Let you focus on data, instead of text format
=============================================================

.. image:: https://api.travis-ci.org/pyexcel/pyexcel-text.svg?branch=master
    :target: http://travis-ci.org/pyexcel/pyexcel-text

.. image:: https://codecov.io/github/pyexcel/pyexcel-xls/coverage.png
    :target: https://codecov.io/github/pyexcel/pyexcel-xls


It is a plugin to `pyexcel <https://github.com/pyexcel/pyexcel>`__ and extends its capbility to present and write data in text fromats mainly through `tabulate`:

* "plain"
* "simple"
* "grid"
* "pipe"
* "orgtbl"
* "rst"
* "mediawiki"
* "latex"
* "latex_booktabs"
* "json"

Usage
======

Here is the example usage::

.. code-block: python

    >>> import pyexcel as pe
    >>> import pyexcel.ext.text as text
    >>> content = [
    ...     ["Column 1", "Column 2", "Column 3"],
    ...     [1, 2, 3],
    ...     [4, 5, 6],
    ...     [7, 8, 9]
    ... ]
    >>> sheet = pe.Sheet(content)
    >>> sheet
    Sheet Name: pyexcel
    --------  --------  --------
    Column 1  Column 2  Column 3
    1         2         3
    4         5         6
    7         8         9
    --------  --------  --------
    >>> sheet.name_columns_by_row(0)
    >>> sheet
    Sheet Name: pyexcel
      Column 1    Column 2    Column 3
    ----------  ----------  ----------
             1           2           3
             4           5           6
             7           8           9
    >>> text.TABLEFMT = "grid"
    >>> sheet
    Sheet Name: pyexcel
    +------------+------------+------------+
    |   Column 1 |   Column 2 |   Column 3 |
    +============+============+============+
    |          1 |          2 |          3 |
    +------------+------------+------------+
    |          4 |          5 |          6 |
    +------------+------------+------------+
    |          7 |          8 |          9 |
    +------------+------------+------------+
    >>> multiple_sheets = {
    ...      'Sheet 1':
    ...          [
    ...              [1.0, 2.0, 3.0],
    ...              [4.0, 5.0, 6.0],
    ...              [7.0, 8.0, 9.0]
    ...          ],
    ...      'Sheet 2':
    ...          [
    ...              ['X', 'Y', 'Z'],
    ...              [1.0, 2.0, 3.0],
    ...              [4.0, 5.0, 6.0]
    ...          ],
    ...      'Sheet 3':
    ...          [
    ...              ['O', 'P', 'Q'],
    ...              [3.0, 2.0, 1.0],
    ...              [4.0, 3.0, 2.0]
    ...          ]
    ...  }
    >>> book = pe.Book(multiple_sheets)
    >>> text.TABLEFMT = "mediawiki"
    >>> book.save_as("myfile.mediawiki")
    >>> myfile = open("myfile.mediawiki")
    >>> print(myfile.read())
    Sheet Name: Sheet 1
    {| class="wikitable" style="text-align: left;"
    |+ <!-- caption -->
    |-
    | align="right"| 1 || align="right"| 2 || align="right"| 3
    |-
    | align="right"| 4 || align="right"| 5 || align="right"| 6
    |-
    | align="right"| 7 || align="right"| 8 || align="right"| 9
    |}
    Sheet Name: Sheet 2
    {| class="wikitable" style="text-align: left;"
    |+ <!-- caption -->
    |-
    | X   || Y   || Z
    |-
    | 1.0 || 2.0 || 3.0
    |-
    | 4.0 || 5.0 || 6.0
    |}
    Sheet Name: Sheet 3
    {| class="wikitable" style="text-align: left;"
    |+ <!-- caption -->
    |-
    | O   || P   || Q
    |-
    | 3.0 || 2.0 || 1.0
    |-
    | 4.0 || 3.0 || 2.0
    |}
    <BLANKLINE>


.. testcode::
   :hide:

    >>> myfile.close()
    >>> import os
    >>> os.unlink("myfile.mediawiki")


Dependencies
============

* tabulate
