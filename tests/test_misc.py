from nose.tools import eq_
import pyexcel as p
from textwrap import dedent


def test_sheet_stream():
    test_data = [[1, 2]]
    stream = p.isave_as(array=test_data, dest_file_type='rst')
    expected = dedent("""
    pyexcel_sheet1:
    =  =
    1  2
    =  =""").strip('\n')
    eq_(stream.getvalue(), expected)


def test_simple_sheet():
    sheet = p.Sheet([[1, 2]])
    eq_(sheet.json, '{"pyexcel sheet": [[1, 2]]}')
