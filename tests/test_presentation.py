import os
from unittest import TestCase
from textwrap import dedent

import pyexcel as pe

from .fixtures import EXPECTED_RESULTS

class TestSimple(TestCase):

    TABLEFMT = 'simple'
    expected_results = EXPECTED_RESULTS['simple']

    def setUp(self):
        self.testfile2 = None

    def _check_presentation(self, name, presentation):

        self.assertTrue(name in self.expected_results,
                        'expected result missing: %s' % presentation)

        expected = self.expected_results[name]
        self.assertEqual(presentation, expected+'\n')

    def test_no_title_multiple_sheets(self):
        adict = {
            'sheet 1': [[1,2],[3,4]],
            'sheet 2': [[5,6],[7,8]]
        }
        book = pe.get_book(bookdict=adict, dest_write_title=False)

        get_presentation_call = getattr(book, "get_%s" % self.TABLEFMT)
        presentation = get_presentation_call(write_title=False)

        self._check_presentation('no_title_multiple_sheets', presentation)

    def test_dict(self):
        adict = {
            'sheet 1': [[1,2],[3,4]],
            'sheet 2': [[5,6],[7,8]]
        }
        book = pe.get_book(bookdict=adict)

        get_presentation_call = getattr(book, "get_%s" % self.TABLEFMT)
        presentation = get_presentation_call()

        self._check_presentation('dict', presentation)

    def test_normal_usage(self):
        content = [
            [1, 2, 3],
            [4, 588, 6],
            [7, 8, 999]
        ]
        sheet = pe.Sheet(content)

        get_presentation_call = getattr(sheet, "get_%s" % self.TABLEFMT)
        presentation = get_presentation_call()

        self._check_presentation('normal_usage', presentation)

    def test_new_normal_usage(self):
        content = [
            [1, 2, 3],
            [4, 588, 6],
            [7, 8, 999]
        ]
        sheet = pe.get_sheet(array=content)

        get_presentation_call = getattr(sheet, "get_%s" % self.TABLEFMT)
        presentation = get_presentation_call()

        self._check_presentation('new_normal_usage', presentation)

    def test_no_title_single_sheet(self):
        content = [
            [1, 2, 3],
            [4, 588, 6],
            [7, 8, 999]
        ]
        sheet = pe.get_sheet(array=content)

        get_presentation_call = getattr(sheet, "get_%s" % self.TABLEFMT)
        presentation = get_presentation_call(write_title=False)

        self._check_presentation('no_title_single_sheet', presentation)

    def test_new_normal_usage_irregular_columns(self):
        content = [
            [1, 2, 3],
            [4, 588, 6],
            [7, 8]
        ]
        sheet = pe.get_sheet(array=content)

        get_presentation_call = getattr(sheet, "get_%s" % self.TABLEFMT)
        presentation = get_presentation_call()

        self._check_presentation('new_normal_usage_irregular_columns', presentation)

    def test_csvbook_irregular_columns(self):
        content = [
            [1, 2, 3],
            [4, 588, 6],
            [7, 8]
        ]
        self.testfile2 = "testfile.csv"
        pe.save_as(array=content, dest_file_name=self.testfile2)
        sheet = pe.get_sheet(file_name=self.testfile2)

        get_presentation_call = getattr(sheet, "get_%s" % self.TABLEFMT)
        presentation = get_presentation_call()

        self._check_presentation('csvbook_irregular_columns', presentation)

    def test_column_series(self):
        content = [
            ["Column 1", "Column 2", "Column 3"],
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        sheet = pe.get_sheet(array=content, name_columns_by_row=0)

        get_presentation_call = getattr(sheet, "get_%s" % self.TABLEFMT)
        presentation = get_presentation_call()

        self._check_presentation('column_series', presentation)

    def test_column_series_irregular_columns(self):
        content = [
            ["Column 1", "Column 2", "Column 3"],
            [1, 2, 3],
            [4, 5, 6],
            [7, 8]
        ]
        sheet = pe.get_sheet(array=content, name_columns_by_row=0)

        get_presentation_call = getattr(sheet, "get_%s" % self.TABLEFMT)
        presentation = get_presentation_call()

        self._check_presentation('column_series_irregular_columns', presentation)

    def test_data_frame(self):
        content = [
            ["", "Column 1", "Column 2", "Column 3"],
            ["Row 1", 1, 2, 3],
            ["Row 2", 4, 5, 6],
            ["Row 3", 7, 8, 9]
        ]
        sheet = pe.get_sheet(array=content, name_rows_by_column=0, name_columns_by_row=0)

        get_presentation_call = getattr(sheet, "get_%s" % self.TABLEFMT)
        presentation = get_presentation_call()

        self._check_presentation('data_frame', presentation)

    def test_row_series(self):
        content = [
            ["Row 1", 1, 2, 3],
            ["Row 2", 4, 5, 6],
            ["Row 3", 7, 8, 9]
        ]

        sheet = pe.get_sheet(array=content, name_rows_by_column=0)

        get_presentation_call = getattr(sheet, "get_%s" % self.TABLEFMT)
        presentation = get_presentation_call()

        self._check_presentation('row_series', presentation)

    def tearDown(self):
        if self.testfile2 and os.path.exists(self.testfile2):
            os.unlink(self.testfile2)


class TestRst(TestSimple):
    TABLEFMT = 'rst'
    expected_results = EXPECTED_RESULTS['rst']


class TestJson(TestSimple):
    TABLEFMT = 'json'
    expected_results = EXPECTED_RESULTS['json']

    def setUp(self):
        TestSimple.setUp(self)
        self.expected_results['csvbook_irregular_columns'] = '{"testfile.csv": [["1", "2", "3"], ["4", "588", "6"], ["7", "8", ""]]}'
        self.expected_results['new_normal_usage_irregular_columns'] = '{"pyexcel_sheet1": [[1, 2, 3], [4, 588, 6], [7, 8, ""]]}'
    def _check_presentation(self, name, presentation):

        self.assertTrue(name in self.expected_results,
                        'expected result missing: %s' % presentation)

        expected = self.expected_results[name]
        self.assertEqual(presentation, expected)



class TestHtml(TestSimple):
    TABLEFMT = 'html'
    expected_results = EXPECTED_RESULTS['html']
    def _check_presentation(self, name, presentation):

        self.assertTrue(name in self.expected_results,
                        'expected result missing: %s' % presentation)

        expected = self.expected_results[name]
        self.assertEqual(presentation, expected+'\n')


class TestCustomJson(TestCase):

    def test_matrix(self):
        content = [
            [1, 2, 3],
            [4, 588, 6],
            [7, 8, 999]
        ]
        s = pe.sheets.Sheet(content)
        content = "{\"pyexcel\": [[1, 2, 3], [4, 588, 6], [7, 8, 999]]}"
        self.assertEqual(s.json, content)

    def test_sheet(self):
        content = [
            [1, 2, 3],
            [4, 588, 6],
            [7, 8, 999]
        ]
        s = pe.Sheet(content, "mytest")
        content = "{\"mytest\": [[1, 2, 3], [4, 588, 6], [7, 8, 999]]}"
        self.assertEqual(s.json, content)

    def test_book_presentation(self):
        data = {
            'Sheet 1':
            [
                [1.0, 2.0, 3.0],
                [4.0, 5.0, 6.0],
                [7.0, 8.0, 9.0]
            ],
            'Sheet 2':
            [
                ['X', 'Y', 'Z'],
                [1.0, 2.0, 3.0],
                [4.0, 5.0, 6.0]
            ],
            'Sheet 3':
            [
                ['O', 'P', 'Q'],
                [3.0, 2.0, 1.0],
                [4.0, 3.0, 2.0]
            ]
        }
        book = pe.Book(data)
        content = '{"Sheet 1": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]], "Sheet 2": [["X", "Y", "Z"], [1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], "Sheet 3": [["O", "P", "Q"], [3.0, 2.0, 1.0], [4.0, 3.0, 2.0]]}'
        self.assertEqual(book.json, content)


class TestPresentation(TestCase):
    def test_normal_usage(self):
        content = [
            [1, 2, 3],
            [4, 588, 6],
            [7, 8, 999]
        ]
        s = pe.Sheet(content)
        content = dedent("""
            Sheet Name: pyexcel
            -  ---  ---
            1    2    3
            4  588    6
            7    8  999
            -  ---  ---""").strip('\n') + '\n'
        self.assertEqual(s.simple, content)
        
    def test_irregular_usage(self):
        """textable doesn't like empty string """
        content = [
            [1, 2, 3],
            [4, 588, 6],
            [7, 8] # one empty string
        ]
        s = pe.Sheet(content)
        content = dedent("""
            Sheet Name: pyexcel
            -  ---  -
            1    2  3
            4  588  6
            7    8
            -  ---  -""").strip('\n') + '\n'
        self.assertEqual(s.simple, content)
    

    def test_column_series(self):
        content = [
            ["Column 1", "Column 2", "Column 3"],
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        s = pe.Sheet(content, name_columns_by_row=0)
        content = dedent("""
            Sheet Name: pyexcel
              Column 1    Column 2    Column 3
            ----------  ----------  ----------
                     1           2           3
                     4           5           6
                     7           8           9""").strip('\n') + '\n'
        self.assertEqual(s.simple, content)

    def test_data_frame(self):
        content = [
            ["", "Column 1", "Column 2", "Column 3"],
            ["Row 1", 1, 2, 3],
            ["Row 2", 4, 5, 6],
            ["Row 3", 7, 8, 9]
        ]
        s = pe.Sheet(content, name_rows_by_column=0, name_columns_by_row=0)
        content = dedent("""
            Sheet Name: pyexcel
                     Column 1    Column 2    Column 3
            -----  ----------  ----------  ----------
            Row 1           1           2           3
            Row 2           4           5           6
            Row 3           7           8           9""").strip('\n') + '\n'
        self.assertEqual(s.simple, content)

    def test_row_series(self):
        content = [
            ["Row 1", 1, 2, 3],
            ["Row 2", 4, 5, 6],
            ["Row 3", 7, 8, 9]
        ]
        s = pe.Sheet(content, name_rows_by_column=0)
        content = dedent("""
            Sheet Name: pyexcel
            -----  -  -  -
            Row 1  1  2  3
            Row 2  4  5  6
            Row 3  7  8  9
            -----  -  -  -""").strip('\n') + '\n'
        self.assertEqual(s.simple, content)

    def test_book_presentation(self):
        data = {
            'Sheet 1':
            [
                [1.0, 2.0, 3.0],
                [4.0, 5.0, 6.0],
                [7.0, 8.0, 9.0]
            ],
            'Sheet 2':
            [
                ['X', 'Y', 'Z'],
                [1.0, 2.0, 3.0],
                [4.0, 5.0, 6.0]
            ],
            'Sheet 3':
            [
                ['O', 'P', 'Q'],
                [3.0, 2.0, 1.0],
                [4.0, 3.0, 2.0]
            ]
        }
        book = pe.Book(data)
        content = dedent("""
            Sheet Name: Sheet 1
            -  -  -
            1  2  3
            4  5  6
            7  8  9
            -  -  -
            Sheet Name: Sheet 2
            ---  ---  ---
            X    Y    Z
            1.0  2.0  3.0
            4.0  5.0  6.0
            ---  ---  ---
            Sheet Name: Sheet 3
            ---  ---  ---
            O    P    Q
            3.0  2.0  1.0
            4.0  3.0  2.0
            ---  ---  ---""").strip("\n") + '\n'
        self.assertEqual(book.simple, content)
