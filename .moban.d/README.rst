================================================================================
{{name}} - Let you focus on data, instead of {{file_type}} formats
================================================================================


{% include "badges.rst.jj2" %}


{%block description%}
It is a plugin to `pyexcel <https://github.com/pyexcel/pyexcel>`__ and extends
its capbility to present and write data in text fromats mainly through `tabulate`:

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
* "html"

Usage
======

What's new?
--------------

.. code-block:: python

    >>> import pyexcel as pe
    >>> sheet = pe.Sheet()
    >>> sheet.json = '[[1,2],[2,3]]'
    >>> sheet
    pyexcel sheet:
    +---+---+
    | 1 | 2 |
    +---+---+
    | 2 | 3 |
    +---+---+
    >>> highspeedrail = pe.Sheet()
    >>> sheet.json = """
    ... [{"year": 1903, "country": "Germany", "speed": "206.7km/h"},
    ... {"year": 1964, "country": "Japan", "speed": "210km/h"},
    ... {"year": 2008, "country": "China", "speed": "350km/h"}]
    ... """
    >>> sheet.name = 'High Speed Train Speed Break Through (Source: Wikipedia)'
    >>> sheet
    High Speed Train Speed Break Through (Source: Wikipedia):
    +---------+-----------+------+
    | country | speed     | year |
    +---------+-----------+------+
    | Germany | 206.7km/h | 1903 |
    +---------+-----------+------+
    | Japan   | 210km/h   | 1964 |
    +---------+-----------+------+
    | China   | 350km/h   | 2008 |
    +---------+-----------+------+

Here is a variant of json:

    >>> highspeedrail2 = pe.Sheet()
    >>> highspeedrail2.ndjson = """
    ... {"year": 1903, "country": "Germany", "speed": "206.7km/h"}
    ... {"year": 1964, "country": "Japan", "speed": "210km/h"}
    ... {"year": 2008, "country": "China", "speed": "350km/h"}
    ... """.strip()
    >>> highspeedrail2.name = 'High Speed Train Speed Break Through (Source: Wikipedia)'
    >>> highspeedrail2
    High Speed Train Speed Break Through (Source: Wikipedia):
    +---------+-----------+------+
    | country | speed     | year |
    +---------+-----------+------+
    | Germany | 206.7km/h | 1903 |
    +---------+-----------+------+
    | Japan   | 210km/h   | 1964 |
    +---------+-----------+------+
    | China   | 350km/h   | 2008 |
    +---------+-----------+------+


Simple
------------

.. code-block:: python

    >>> import pyexcel as pe
    >>> content = [
    ...     ["Column 1", "Column 2", "Column 3"],
    ...     [1, 2, 3],
    ...     [4, 5, 6],
    ...     [7, 8, 9]
    ... ]
    >>> sheet = pe.Sheet(content)
    >>> print(sheet.simple)
    pyexcel sheet:
    --------  --------  --------
    Column 1  Column 2  Column 3
    1         2         3
    4         5         6
    7         8         9
    --------  --------  --------
    >>> sheet.name_columns_by_row(0)
    >>> print(sheet.simple)
    pyexcel sheet:
      Column 1    Column 2    Column 3
    ----------  ----------  ----------
             1           2           3
             4           5           6
             7           8           9


Grid
-------

.. code-block:: python

    >>> print(sheet.grid)
    pyexcel sheet:
    +------------+------------+------------+
    |   Column 1 |   Column 2 |   Column 3 |
    +============+============+============+
    |          1 |          2 |          3 |
    +------------+------------+------------+
    |          4 |          5 |          6 |
    +------------+------------+------------+
    |          7 |          8 |          9 |
    +------------+------------+------------+


Mediawiki
-------------

.. code-block:: python

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
    >>> book.save_as("myfile.mediawiki")
    >>> myfile = open("myfile.mediawiki")
    >>> print(myfile.read())
    Sheet 1:
    {| class="wikitable" style="text-align: left;"
    |+ <!-- caption -->
    |-
    | align="right"| 1 || align="right"| 2 || align="right"| 3
    |-
    | align="right"| 4 || align="right"| 5 || align="right"| 6
    |-
    | align="right"| 7 || align="right"| 8 || align="right"| 9
    |}
    Sheet 2:
    {| class="wikitable" style="text-align: left;"
    |+ <!-- caption -->
    |-
    | X   || Y   || Z
    |-
    | 1.0 || 2.0 || 3.0
    |-
    | 4.0 || 5.0 || 6.0
    |}
    Sheet 3:
    {| class="wikitable" style="text-align: left;"
    |+ <!-- caption -->
    |-
    | O   || P   || Q
    |-
    | 3.0 || 2.0 || 1.0
    |-
    | 4.0 || 3.0 || 2.0
    |}
    >>> myfile.close()

Html
----------

.. code-block:: python

    >>> book.save_as("myfile.html")
    >>> myfile = open("myfile.html")
    >>> print(myfile.read()) # doctest: +SKIP
    Sheet 1:
    <table>
    <tr><td style="text-align: right;">1</td><td style="text-align: right;">2</td><td style="text-align: right;">3</td></tr>
    <tr><td style="text-align: right;">4</td><td style="text-align: right;">5</td><td style="text-align: right;">6</td></tr>
    <tr><td style="text-align: right;">7</td><td style="text-align: right;">8</td><td style="text-align: right;">9</td></tr>
    </table>
    Sheet 2:
    <table>
    <tr><td>X  </td><td>Y  </td><td>Z  </td></tr>
    <tr><td>1.0</td><td>2.0</td><td>3.0</td></tr>
    <tr><td>4.0</td><td>5.0</td><td>6.0</td></tr>
    </table>
    Sheet 3:
    <table>
    <tr><td>O  </td><td>P  </td><td>Q  </td></tr>
    <tr><td>3.0</td><td>2.0</td><td>1.0</td></tr>
    <tr><td>4.0</td><td>3.0</td><td>2.0</td></tr>
    </table>

Please note tabulate 0.7.7 gives an extra tbody tag around tr tag.

.. testcode::
   :hide:

    >>> myfile.close()
    >>> import os
    >>> os.unlink("myfile.mediawiki")
    >>> os.unlink("myfile.html")

{%endblock%}

{%block extras %}
Dependencies
============

* tabulate
{%endblock%}
