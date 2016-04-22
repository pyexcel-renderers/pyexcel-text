import platform
from distutils.version import LooseVersion
from textwrap import dedent
import tabulate


EXPECTED_RESULTS = {
    'simple': {
        'dict': dedent("""
            Sheet Name: sheet 1
            -  -
            1  2
            3  4
            -  -
            Sheet Name: sheet 2
            -  -
            5  6
            7  8
            -  -""").strip('\n'),
        'no_title_multiple_sheets': dedent("""
            -  -
            1  2
            3  4
            -  -
            -  -
            5  6
            7  8
            -  -""").strip('\n'),
        'normal_usage': dedent("""
            Sheet Name: pyexcel
            -  ---  ---
            1    2    3
            4  588    6
            7    8  999
            -  ---  ---""").strip('\n'),
        'new_normal_usage': dedent("""
            Sheet Name: pyexcel_sheet1
            -  ---  ---
            1    2    3
            4  588    6
            7    8  999
            -  ---  ---""").strip('\n'),
        'no_title_single_sheet': dedent("""
            -  ---  ---
            1    2    3
            4  588    6
            7    8  999
            -  ---  ---""").strip('\n'),
        'new_normal_usage_irregular_columns': dedent("""
            Sheet Name: pyexcel_sheet1
            -  ---  -
            1    2  3
            4  588  6
            7    8
            -  ---  -""").strip('\n'),
        'csvbook_irregular_columns': dedent("""
            Sheet Name: testfile.csv
            -  ---  -
            1    2  3
            4  588  6
            7    8
            -  ---  -""").strip('\n'),
        'column_series': dedent("""
            Sheet Name: pyexcel_sheet1
              Column 1    Column 2    Column 3
            ----------  ----------  ----------
                     1           2           3
                     4           5           6
                     7           8           9""").strip('\n'),
         # FIXME: numerical align lost when one cell is missing
         'column_series_irregular_columns': dedent("""
            Sheet Name: pyexcel_sheet1
              Column 1    Column 2  Column 3
            ----------  ----------  ----------
                     1           2  3
                     4           5  6
                     7           8""").strip('\n'),
        'data_frame': dedent("""
            Sheet Name: pyexcel_sheet1
                     Column 1    Column 2    Column 3
            -----  ----------  ----------  ----------
            Row 1           1           2           3
            Row 2           4           5           6
            Row 3           7           8           9""").strip('\n'),
         'row_series': dedent("""
            Sheet Name: pyexcel_sheet1
            -----  -  -  -
            Row 1  1  2  3
            Row 2  4  5  6
            Row 3  7  8  9
            -----  -  -  -""").strip('\n')
    },
    "rst":{
        'dict': dedent("""
            Sheet Name: sheet 1
            =  =
            1  2
            3  4
            =  =
            Sheet Name: sheet 2
            =  =
            5  6
            7  8
            =  =""").strip('\n'),
        'no_title_multiple_sheets': dedent("""
            =  =
            1  2
            3  4
            =  =
            =  =
            5  6
            7  8
            =  =""").strip('\n'),
        'normal_usage': dedent("""
            Sheet Name: pyexcel
            =  ===  ===
            1    2    3
            4  588    6
            7    8  999
            =  ===  ===""").strip('\n'),
        'new_normal_usage': dedent("""
            Sheet Name: pyexcel_sheet1
            =  ===  ===
            1    2    3
            4  588    6
            7    8  999
            =  ===  ===""").strip('\n'),
        'no_title_single_sheet': dedent("""
            =  ===  ===
            1    2    3
            4  588    6
            7    8  999
            =  ===  ===""").strip('\n'),
        'new_normal_usage_irregular_columns': dedent("""
            Sheet Name: pyexcel_sheet1
            =  ===  =
            1    2  3
            4  588  6
            7    8
            =  ===  =""").strip('\n'),
        'column_series': dedent("""
            Sheet Name: pyexcel_sheet1
            ==========  ==========  ==========
              Column 1    Column 2    Column 3
            ==========  ==========  ==========
                     1           2           3
                     4           5           6
                     7           8           9
            ==========  ==========  ==========""").strip('\n'),
        'column_series_irregular_columns': dedent("""
            Sheet Name: pyexcel_sheet1
            ==========  ==========  ==========
              Column 1    Column 2  Column 3
            ==========  ==========  ==========
                     1           2  3
                     4           5  6
                     7           8
            ==========  ==========  ==========""").strip('\n'),
        'csvbook_irregular_columns': dedent("""
            Sheet Name: testfile.csv
            =  ===  =
            1    2  3
            4  588  6
            7    8
            =  ===  =""").strip('\n'),
        'row_series': dedent("""
            Sheet Name: pyexcel_sheet1
            =====  =  =  =
            Row 1  1  2  3
            Row 2  4  5  6
            Row 3  7  8  9
            =====  =  =  =""").strip('\n')
    },
    'html': {
        'dict': dedent("""
            <html><header><title>testfile.html</title><body>Sheet Name: sheet 1
            <table>
            <tr><td style="text-align: right;">1</td><td style="text-align: right;">2</td></tr>
            <tr><td style="text-align: right;">3</td><td style="text-align: right;">4</td></tr>
            </table>
            Sheet Name: sheet 2
            <table>
            <tr><td style="text-align: right;">5</td><td style="text-align: right;">6</td></tr>
            <tr><td style="text-align: right;">7</td><td style="text-align: right;">8</td></tr>
            </table>
            </body></html>""").strip('\n'),
        'no_title_multiple_sheets': dedent("""
            <html><header><title>testfile.html</title><body><table>
            <tr><td style="text-align: right;">1</td><td style="text-align: right;">2</td></tr>
            <tr><td style="text-align: right;">3</td><td style="text-align: right;">4</td></tr>
            </table>
            <table>
            <tr><td style="text-align: right;">5</td><td style="text-align: right;">6</td></tr>
            <tr><td style="text-align: right;">7</td><td style="text-align: right;">8</td></tr>
            </table>
            </body></html>""").strip('\n'),
        'normal_usage': dedent("""
            <html><header><title>testfile.html</title><body>Sheet Name: pyexcel
            <table>
            <tr><td style="text-align: right;">1</td><td style="text-align: right;">  2</td><td style="text-align: right;">  3</td></tr>
            <tr><td style="text-align: right;">4</td><td style="text-align: right;">588</td><td style="text-align: right;">  6</td></tr>
            <tr><td style="text-align: right;">7</td><td style="text-align: right;">  8</td><td style="text-align: right;">999</td></tr>
            </table>
            </body></html>""").strip('\n'),
        'new_normal_usage': dedent("""
            <html><header><title>testfile.html</title><body>Sheet Name: pyexcel_sheet1
            <table>
            <tr><td style="text-align: right;">1</td><td style="text-align: right;">  2</td><td style="text-align: right;">  3</td></tr>
            <tr><td style="text-align: right;">4</td><td style="text-align: right;">588</td><td style="text-align: right;">  6</td></tr>
            <tr><td style="text-align: right;">7</td><td style="text-align: right;">  8</td><td style="text-align: right;">999</td></tr>
            </table>
            </body></html>""").strip('\n'),
        'no_title_single_sheet': dedent("""
            <html><header><title>testfile.html</title><body><table>
            <tr><td style="text-align: right;">1</td><td style="text-align: right;">  2</td><td style="text-align: right;">  3</td></tr>
            <tr><td style="text-align: right;">4</td><td style="text-align: right;">588</td><td style="text-align: right;">  6</td></tr>
            <tr><td style="text-align: right;">7</td><td style="text-align: right;">  8</td><td style="text-align: right;">999</td></tr>
            </table>
            </body></html>""").strip('\n'),
        'new_normal_usage_irregular_columns': dedent("""
            <html><header><title>testfile.html</title><body>Sheet Name: pyexcel_sheet1
            <table>
            <tr><td style="text-align: right;">1</td><td style="text-align: right;">  2</td><td>3</td></tr>
            <tr><td style="text-align: right;">4</td><td style="text-align: right;">588</td><td>6</td></tr>
            <tr><td style="text-align: right;">7</td><td style="text-align: right;">  8</td><td> </td></tr>
            </table>
            </body></html>""").strip('\n'),
        'column_series': dedent("""
            <html><header><title>testfile.html</title><body>Sheet Name: pyexcel_sheet1
            <table>
            <tr><th style="text-align: right;">  Column 1</th><th style="text-align: right;">  Column 2</th><th style="text-align: right;">  Column 3</th></tr>
            <tr><td style="text-align: right;">         1</td><td style="text-align: right;">         2</td><td style="text-align: right;">         3</td></tr>
            <tr><td style="text-align: right;">         4</td><td style="text-align: right;">         5</td><td style="text-align: right;">         6</td></tr>
            <tr><td style="text-align: right;">         7</td><td style="text-align: right;">         8</td><td style="text-align: right;">         9</td></tr>
            </table>
            </body></html>""").strip('\n'),
        'column_series_irregular_columns': dedent("""
            <html><header><title>testfile.html</title><body>Sheet Name: pyexcel_sheet1
            <table>
            <tr><th style="text-align: right;">  Column 1</th><th style="text-align: right;">  Column 2</th><th>Column 3  </th></tr>
            <tr><td style="text-align: right;">         1</td><td style="text-align: right;">         2</td><td>3         </td></tr>
            <tr><td style="text-align: right;">         4</td><td style="text-align: right;">         5</td><td>6         </td></tr>
            <tr><td style="text-align: right;">         7</td><td style="text-align: right;">         8</td><td>          </td></tr>
            </table>
            </body></html>""").strip('\n'),
        'csvbook_irregular_columns': dedent("""
            <html><header><title>testfile.html</title><body>Sheet Name: testfile.csv
            <table>
            <tr><td style="text-align: right;">1</td><td style="text-align: right;">  2</td><td>3</td></tr>
            <tr><td style="text-align: right;">4</td><td style="text-align: right;">588</td><td>6</td></tr>
            <tr><td style="text-align: right;">7</td><td style="text-align: right;">  8</td><td> </td></tr>
            </table>
            </body></html>""").strip('\n'),
        'data_frame': dedent("""
            <html><header><title>testfile.html</title><body>Sheet Name: pyexcel_sheet1
            <table>
            <tr><th>     </th><th style="text-align: right;">  Column 1</th><th style="text-align: right;">  Column 2</th><th style="text-align: right;">  Column 3</th></tr>
            <tr><td>Row 1</td><td style="text-align: right;">         1</td><td style="text-align: right;">         2</td><td style="text-align: right;">         3</td></tr>
            <tr><td>Row 2</td><td style="text-align: right;">         4</td><td style="text-align: right;">         5</td><td style="text-align: right;">         6</td></tr>
            <tr><td>Row 3</td><td style="text-align: right;">         7</td><td style="text-align: right;">         8</td><td style="text-align: right;">         9</td></tr>
            </table>
            </body></html>""").strip('\n'),
        'row_series': dedent("""
            <html><header><title>testfile.html</title><body>Sheet Name: pyexcel_sheet1
            <table>
            <tr><td>Row 1</td><td style="text-align: right;">1</td><td style="text-align: right;">2</td><td style="text-align: right;">3</td></tr>
            <tr><td>Row 2</td><td style="text-align: right;">4</td><td style="text-align: right;">5</td><td style="text-align: right;">6</td></tr>
            <tr><td>Row 3</td><td style="text-align: right;">7</td><td style="text-align: right;">8</td><td style="text-align: right;">9</td></tr>
            </table>
            </body></html>
            """).strip('\n'),
    },
    'json':{
        'dict':
            '{"sheet 1": [[1, 2], [3, 4]], "sheet 2": [[5, 6], [7, 8]]}',
        'no_title_multiple_sheets':
            '{"sheet 1": [[1, 2], [3, 4]], "sheet 2": [[5, 6], [7, 8]]}',
        'normal_usage':
            '{"pyexcel": [[1, 2, 3], [4, 588, 6], [7, 8, 999]]}',
        'new_normal_usage':
            '{"pyexcel_sheet1": [[1, 2, 3], [4, 588, 6], [7, 8, 999]]}',
        'no_title_single_sheet':
            '[[1, 2, 3], [4, 588, 6], [7, 8, 999]]',
        'new_normal_usage_irregular_columns':
            '{"pyexcel_sheet1": [[1, 2, 3], [4, 588, 6], [7, 8]]}',
        'column_series':
            '{"pyexcel_sheet1": [{"Column 1": 1, "Column 2": 2, "Column 3": 3},'
            ' {"Column 1": 4, "Column 2": 5, "Column 3": 6},'
            ' {"Column 1": 7, "Column 2": 8, "Column 3": 9}]}',
        'column_series_irregular_columns':
            '{"pyexcel_sheet1": [{"Column 1": 1, "Column 2": 2, "Column 3": 3},'
            ' {"Column 1": 4, "Column 2": 5, "Column 3": 6},'
            ' {"Column 1": 7, "Column 2": 8, "Column 3": ""}]}',
        'csvbook_irregular_columns':
            '{"testfile.csv": [["1", "2", "3"], ["4", "588", "6"], ["7", "8"]]}',
        'data_frame':
            '{"pyexcel_sheet1": {"Row 1": {"Column 1": 1, "Column 2": 2, "Column 3": 3}, "Row 2": {"Column 1": 4, "Column 2": 5, "Column 3": 6}, "Row 3": {"Column 1": 7, "Column 2": 8, "Column 3": 9}}}',
        'row_series':
            '{"pyexcel_sheet1": {"Row 1": [1, 2, 3], "Row 2": [4, 5, 6], "Row 3": [7, 8, 9]}}',
    }
}

if (LooseVersion(tabulate.__version__) <= LooseVersion('0.7.5') or
    platform.python_implementation() == 'PyPy'):
    EXPECTED_RESULTS['rst']['data_frame'] = dedent("""
            Sheet Name: pyexcel_sheet1
            =====  ==========  ==========  ==========
                     Column 1    Column 2    Column 3
            =====  ==========  ==========  ==========
            Row 1           1           2           3
            Row 2           4           5           6
            Row 3           7           8           9
            =====  ==========  ==========  ==========""").strip('\n')
else:
    EXPECTED_RESULTS['rst']['data_frame'] = dedent("""
            Sheet Name: pyexcel_sheet1
            =====  ==========  ==========  ==========
            ..       Column 1    Column 2    Column 3
            =====  ==========  ==========  ==========
            Row 1           1           2           3
            Row 2           4           5           6
            Row 3           7           8           9
            =====  ==========  ==========  ==========""").strip('\n')


# tabulate 0.7.6-dev adds <thead> and <tbody> elements
if LooseVersion(tabulate.__version__) > LooseVersion('0.7.5'):
    EXPECTED_RESULTS['html'] = dict(
            (key, value.replace('<tr><th ', '<thead>\n<tr><th ').replace('<tr><th>', '<thead>\n<tr><th>').replace('</th></tr>', '</th></tr>\n</thead>\n<tbody>').replace('<table>\n<tr>', '<table>\n<tbody>\n<tr>').replace('</table>', '</tbody>\n</table>'))
            for key, value in EXPECTED_RESULTS['html'].items())
