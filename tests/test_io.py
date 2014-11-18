import os
import sys
from textwrap import dedent
import pyexcel as pe
from pyexcel.ext import text
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

class TestIO:
    def setUp(self):
        self.testfile = "testfile.txt"
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
        print(written_content)
        assert written_content == content

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


class TestStream:
    def setUp(self):
        self.testfile = StringIO()
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
        print(written_content)
        assert written_content == content