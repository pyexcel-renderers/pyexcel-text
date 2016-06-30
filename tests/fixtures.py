import platform
from distutils.version import LooseVersion
from textwrap import dedent
import tabulate
# flake8: noqa

EXPECTED_RESULTS = {
    'simple': {
        'dict': dedent("""
            sheet 1:
            -  -
            1  2
            3  4
            -  -
            sheet 2:
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
            pyexcel sheet:
            -  ---  ---
            1    2    3
            4  588    6
            7    8  999
            -  ---  ---""").strip('\n'),
        'new_normal_usage': dedent("""
            pyexcel_sheet1:
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
            pyexcel_sheet1:
            -  ---  -
            1    2  3
            4  588  6
            7    8
            -  ---  -""").strip('\n'),
        'csvbook_irregular_columns': dedent("""
            testfile.csv:
            -  ---  -
            1    2  3
            4  588  6
            7    8
            -  ---  -""").strip('\n'),
        'column_series': dedent("""
            pyexcel_sheet1:
              Column 1    Column 2    Column 3
            ----------  ----------  ----------
                     1           2           3
                     4           5           6
                     7           8           9""").strip('\n'),
         # FIXME: numerical align lost when one cell is missing
         'column_series_irregular_columns': dedent("""
            pyexcel_sheet1:
              Column 1    Column 2  Column 3
            ----------  ----------  ----------
                     1           2  3
                     4           5  6
                     7           8""").strip('\n'),
        'data_frame': dedent("""
            pyexcel_sheet1:
                     Column 1    Column 2    Column 3
            -----  ----------  ----------  ----------
            Row 1           1           2           3
            Row 2           4           5           6
            Row 3           7           8           9""").strip('\n'),
         'row_series': dedent("""
            pyexcel_sheet1:
            -----  -  -  -
            Row 1  1  2  3
            Row 2  4  5  6
            Row 3  7  8  9
            -----  -  -  -""").strip('\n')
    },
    "rst":{
        'dict': dedent("""
            sheet 1:
            =  =
            1  2
            3  4
            =  =
            sheet 2:
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
            pyexcel sheet:
            =  ===  ===
            1    2    3
            4  588    6
            7    8  999
            =  ===  ===""").strip('\n'),
        'new_normal_usage': dedent("""
            pyexcel_sheet1:
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
            pyexcel_sheet1:
            =  ===  =
            1    2  3
            4  588  6
            7    8
            =  ===  =""").strip('\n'),
        'column_series': dedent("""
            pyexcel_sheet1:
            ==========  ==========  ==========
              Column 1    Column 2    Column 3
            ==========  ==========  ==========
                     1           2           3
                     4           5           6
                     7           8           9
            ==========  ==========  ==========""").strip('\n'),
        'column_series_irregular_columns': dedent("""
            pyexcel_sheet1:
            ==========  ==========  ==========
              Column 1    Column 2  Column 3
            ==========  ==========  ==========
                     1           2  3
                     4           5  6
                     7           8
            ==========  ==========  ==========""").strip('\n'),
        'csvbook_irregular_columns': dedent("""
            testfile.csv:
            =  ===  =
            1    2  3
            4  588  6
            7    8
            =  ===  =""").strip('\n'),
        'row_series': dedent("""
            pyexcel_sheet1:
            =====  =  =  =
            Row 1  1  2  3
            Row 2  4  5  6
            Row 3  7  8  9
            =====  =  =  =""").strip('\n')
    },
    'html': {
        'dict': dedent("""
            sheet 1:
            <table>
            <tr><td style="text-align: right;">1</td><td style="text-align: right;">2</td></tr>
            <tr><td style="text-align: right;">3</td><td style="text-align: right;">4</td></tr>
            </table>
            sheet 2:
            <table>
            <tr><td style="text-align: right;">5</td><td style="text-align: right;">6</td></tr>
            <tr><td style="text-align: right;">7</td><td style="text-align: right;">8</td></tr>
            </table>""").strip('\n'),
        'no_title_multiple_sheets': dedent("""
            <table>
            <tr><td style="text-align: right;">1</td><td style="text-align: right;">2</td></tr>
            <tr><td style="text-align: right;">3</td><td style="text-align: right;">4</td></tr>
            </table>
            <table>
            <tr><td style="text-align: right;">5</td><td style="text-align: right;">6</td></tr>
            <tr><td style="text-align: right;">7</td><td style="text-align: right;">8</td></tr>
            </table>""").strip('\n'),
        'normal_usage': dedent("""
            pyexcel sheet:
            <table>
            <tr><td style="text-align: right;">1</td><td style="text-align: right;">  2</td><td style="text-align: right;">  3</td></tr>
            <tr><td style="text-align: right;">4</td><td style="text-align: right;">588</td><td style="text-align: right;">  6</td></tr>
            <tr><td style="text-align: right;">7</td><td style="text-align: right;">  8</td><td style="text-align: right;">999</td></tr>
            </table>""").strip('\n'),
        'new_normal_usage': dedent("""
            pyexcel_sheet1:
            <table>
            <tr><td style="text-align: right;">1</td><td style="text-align: right;">  2</td><td style="text-align: right;">  3</td></tr>
            <tr><td style="text-align: right;">4</td><td style="text-align: right;">588</td><td style="text-align: right;">  6</td></tr>
            <tr><td style="text-align: right;">7</td><td style="text-align: right;">  8</td><td style="text-align: right;">999</td></tr>
            </table>""").strip('\n'),
        'no_title_single_sheet': dedent("""
            <table>
            <tr><td style="text-align: right;">1</td><td style="text-align: right;">  2</td><td style="text-align: right;">  3</td></tr>
            <tr><td style="text-align: right;">4</td><td style="text-align: right;">588</td><td style="text-align: right;">  6</td></tr>
            <tr><td style="text-align: right;">7</td><td style="text-align: right;">  8</td><td style="text-align: right;">999</td></tr>
            </table>""").strip('\n'),
        'new_normal_usage_irregular_columns': dedent("""
            pyexcel_sheet1:
            <table>
            <tr><td style="text-align: right;">1</td><td style="text-align: right;">  2</td><td>3</td></tr>
            <tr><td style="text-align: right;">4</td><td style="text-align: right;">588</td><td>6</td></tr>
            <tr><td style="text-align: right;">7</td><td style="text-align: right;">  8</td><td> </td></tr>
            </table>""").strip('\n'),
        'column_series': dedent("""
            pyexcel_sheet1:
            <table>
            <tr><th style="text-align: right;">  Column 1</th><th style="text-align: right;">  Column 2</th><th style="text-align: right;">  Column 3</th></tr>
            <tr><td style="text-align: right;">         1</td><td style="text-align: right;">         2</td><td style="text-align: right;">         3</td></tr>
            <tr><td style="text-align: right;">         4</td><td style="text-align: right;">         5</td><td style="text-align: right;">         6</td></tr>
            <tr><td style="text-align: right;">         7</td><td style="text-align: right;">         8</td><td style="text-align: right;">         9</td></tr>
            </table>""").strip('\n'),
        'column_series_irregular_columns': dedent("""
            pyexcel_sheet1:
            <table>
            <tr><th style="text-align: right;">  Column 1</th><th style="text-align: right;">  Column 2</th><th>Column 3  </th></tr>
            <tr><td style="text-align: right;">         1</td><td style="text-align: right;">         2</td><td>3         </td></tr>
            <tr><td style="text-align: right;">         4</td><td style="text-align: right;">         5</td><td>6         </td></tr>
            <tr><td style="text-align: right;">         7</td><td style="text-align: right;">         8</td><td>          </td></tr>
            </table>""").strip('\n'),
        'csvbook_irregular_columns': dedent("""
            testfile.csv:
            <table>
            <tr><td style="text-align: right;">1</td><td style="text-align: right;">  2</td><td>3</td></tr>
            <tr><td style="text-align: right;">4</td><td style="text-align: right;">588</td><td>6</td></tr>
            <tr><td style="text-align: right;">7</td><td style="text-align: right;">  8</td><td> </td></tr>
            </table>""").strip('\n'),
        'data_frame': dedent("""
            pyexcel_sheet1:
            <table>
            <tr><th>     </th><th style="text-align: right;">  Column 1</th><th style="text-align: right;">  Column 2</th><th style="text-align: right;">  Column 3</th></tr>
            <tr><td>Row 1</td><td style="text-align: right;">         1</td><td style="text-align: right;">         2</td><td style="text-align: right;">         3</td></tr>
            <tr><td>Row 2</td><td style="text-align: right;">         4</td><td style="text-align: right;">         5</td><td style="text-align: right;">         6</td></tr>
            <tr><td>Row 3</td><td style="text-align: right;">         7</td><td style="text-align: right;">         8</td><td style="text-align: right;">         9</td></tr>
            </table>""").strip('\n'),
        'row_series': dedent("""
            pyexcel_sheet1:
            <table>
            <tr><td>Row 1</td><td style="text-align: right;">1</td><td style="text-align: right;">2</td><td style="text-align: right;">3</td></tr>
            <tr><td>Row 2</td><td style="text-align: right;">4</td><td style="text-align: right;">5</td><td style="text-align: right;">6</td></tr>
            <tr><td>Row 3</td><td style="text-align: right;">7</td><td style="text-align: right;">8</td><td style="text-align: right;">9</td></tr>
            </table>""").strip('\n'),
    },
    'json':{
        'dict':
            '{"sheet 1": [[1, 2], [3, 4]], "sheet 2": [[5, 6], [7, 8]]}',
        'no_title_multiple_sheets':
            '{"sheet 1": [[1, 2], [3, 4]], "sheet 2": [[5, 6], [7, 8]]}',
        'normal_usage':
            '{"pyexcel sheet": [[1, 2, 3], [4, 588, 6], [7, 8, 999]]}',
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
            '{"testfile.csv": [[1, 2, 3], [4, 588, 6], [7, 8]]}',
        'data_frame':
            '{"pyexcel_sheet1": {"Row 1": {"Column 1": 1, "Column 2": 2, "Column 3": 3}, "Row 2": {"Column 1": 4, "Column 2": 5, "Column 3": 6}, "Row 3": {"Column 1": 7, "Column 2": 8, "Column 3": 9}}}',
        'row_series':
            '{"pyexcel_sheet1": [{"Row 1": 1, "Row 2": 4, "Row 3": 7}, {"Row 1": 2, "Row 2": 5, "Row 3": 8}, {"Row 1": 3, "Row 2": 6, "Row 3": 9}]}'
    }
}

if (LooseVersion(tabulate.__version__) <= LooseVersion('0.7.5') or
    platform.python_implementation() == 'PyPy'):
    EXPECTED_RESULTS['rst']['data_frame'] = dedent("""
            pyexcel_sheet1:
            =====  ==========  ==========  ==========
                     Column 1    Column 2    Column 3
            =====  ==========  ==========  ==========
            Row 1           1           2           3
            Row 2           4           5           6
            Row 3           7           8           9
            =====  ==========  ==========  ==========""").strip('\n')
else:
    EXPECTED_RESULTS['rst']['data_frame'] = dedent("""
            pyexcel_sheet1:
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
