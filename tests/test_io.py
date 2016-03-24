import os
import sys
import json

from textwrap import dedent
import pyexcel as pe
from pyexcel.ext import text
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

class TestIO:
    def setUp(self):
        self.testfile = "testfile.simple"
        self.testfile2 = None
        text.TABLEFMT = "simple"
    def test_normal_usage(self):
        content = [
            [1, 2, 3],
            [4, 588, 6],
            [7, 8, 999]
        ]
        s = pe.Sheet(content)
        text.save_as(s, self.testfile)
        f = open(self.testfile, "r")
        written_content = f.read()
        f.close()
        content = dedent("""
            Sheet Name: pyexcel
            -  ---  ---
            1    2    3
            4  588    6
            7    8  999
            -  ---  ---""").strip('\n')
        assert written_content == content

    def test_new_normal_usage(self):
        content = [
            [1, 2, 3],
            [4, 588, 6],
            [7, 8, 999]
        ]
        pe.save_as(array=content, dest_file_name=self.testfile)
        f = open(self.testfile, "r")
        written_content = f.read()
        f.close()
        content = dedent("""
            Sheet Name: pyexcel_sheet1
            -  ---  ---
            1    2    3
            4  588    6
            7    8  999
            -  ---  ---""").strip('\n')
        assert written_content.strip('\n') == content

    def test_new_normal_usage_irregular_columns(self):
        content = [
            [1, 2, 3],
            [4, 588, 6],
            [7, 8]
        ]
        pe.save_as(array=content, dest_file_name=self.testfile)
        f = open(self.testfile, "r")
        written_content = f.read()
        f.close()
        content = dedent("""
            Sheet Name: pyexcel_sheet1
            -  ---  -
            1    2  3
            4  588  6
            7    8
            -  ---  -""").strip('\n')
        print(written_content)
        assert written_content.strip('\n') == content

    def test_csvbook_irregular_columns(self):
        content = [
            [1, 2, 3],
            [4, 588, 6],
            [7, 8]
        ]
        self.testfile2 = "testfile.csv"
        pe.save_as(array=content, dest_file_name=self.testfile2)
        pe.save_as(file_name=self.testfile2, dest_file_name=self.testfile)

        f = open(self.testfile, "r")
        written_content = f.read()
        f.close()

        content = dedent("""
            Sheet Name: testfile.csv
            -  ---  -
            1    2  3
            4  588  6
            7    8
            -  ---  -""").strip('\n')
        assert written_content.strip('\n') == content

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
        if self.testfile2 and os.path.exists(self.testfile2):
            os.unlink(self.testfile2)

class TestRst:
    def setUp(self):
        self.testfile = "testfile.rst"

    def test_new_normal_usage(self):
        content = [
            [1, 2, 3],
            [4, 588, 6],
            [7, 8, 999]
        ]
        pe.save_as(array=content, dest_file_name=self.testfile)
        f = open(self.testfile, "r")
        written_content = f.read()
        f.close()
        content = dedent("""
        Sheet Name: pyexcel_sheet1
        =  ===  ===
        1    2    3
        4  588    6
        7    8  999
        =  ===  ===""").strip('\n')
        assert written_content.strip('\n') == content

    def test_dict(self):
        adict = {
            'sheet 1': [[1,2],[3,4]],
            'sheet 2': [[5,6],[7,8]]
        }
        pe.save_book_as(bookdict=adict, dest_file_name=self.testfile)
        f = open(self.testfile, "r")
        written_content = f.read()
        f.close()
        content = dedent("""
        Sheet Name: sheet 1
        =  =
        1  2
        3  4
        =  =
        Sheet Name: sheet 2
        =  =
        5  6
        7  8
        =  =""").strip('\n')
        assert written_content.strip('\n') == content

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)

class TestJSON:
    def setUp(self):
        self.testfile = "testfile.json"

    def test_new_normal_usage(self):
        content = [
            [1, 2, 3],
            [4, 588, 6],
            [7, 8, 999]
        ]
        pe.save_as(array=content, dest_file_name=self.testfile)
        with open(self.testfile, "r") as f:
            written_content = json.load(f)
            assert written_content == content

    def test_dict(self):
        adict = {
            'sheet 1': [[1,2],[3,4]],
            'sheet 2': [[5,6],[7,8]]
        }
        pe.save_book_as(bookdict=adict, dest_file_name=self.testfile)
        with open(self.testfile, "r") as f:
            written_content = json.load(f)
            assert written_content == adict

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


class TestStream:
    def setUp(self):
        self.testfile = StringIO()
        text.TABLEFMT = "simple"
    def test_normal_usage(self):
        content = [
            [1, 2, 3],
            [4, 588, 6],
            [7, 8, 999]
        ]
        s = pe.Sheet(content)
        text.save_to_memory(s, self.testfile)
        written_content = self.testfile.getvalue()
        content = dedent("""
            Sheet Name: pyexcel
            -  ---  ---
            1    2    3
            4  588    6
            7    8  999
            -  ---  ---""").strip('\n')
        assert written_content == content
