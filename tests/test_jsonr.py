import os
from nose.tools import eq_
from pyexcel._compact import StringIO
from pyexcel_text.jsonr import JsonParser


class TestStructure:

    def setUp(self):
        self.parser = JsonParser("json")

    def test_dict(self):
        sheet_name = 'test'
        self.content = self.parser.parse_file(get_file("dict.json"),
                                              sheet_name=sheet_name)
        expected = {
            sheet_name: [
                ['a', 'b', 'c'],
                [1, 2, 4],
                [2, 3, 5]
            ]
        }
        self._verify(expected)

    def test_records(self):
        sheet_name = 'test'
        self.content = self.parser.parse_file(get_file("records.json"),
                                              sheet_name=sheet_name)
        expected = {
            sheet_name: [
                ['a', 'b', 'c'],
                [1, 2, 3],
                [1, 2, 4]
            ]
        }
        self._verify(expected)

    def test_book_dict(self):
        sheet_name = 'test'
        self.content = self.parser.parse_file(get_file("bookdict.json"),
                                              sheet_name=sheet_name)
        expected = {
            'sheet 1': [[1, 2], [2, 3]],
            'sheet 2': [[1, 2], [3, 4]]
        }

        self._verify(expected)

    def _verify(self, expected):
        for key in self.content:
            self.content[key] = list(self.content[key])
        eq_(self.content, expected)


class TestMedia:

    def setUp(self):
        self.parser = JsonParser("json")

    def test_file(self):
        self.content = self.parser.parse_file(get_file("array.json"),
                                              sheet_name='test')
        self._verify()

    def test_stream(self):
        with open(get_file("array.json"), 'r') as f:
            file_stream = StringIO(f.read())
        self.content = self.parser.parse_file_stream(file_stream,
                                                     sheet_name='test')
        self._verify()

    def test_content(self):
        with open(get_file("array.json"), 'r') as f:
            file_content = f.read()
        self.content = self.parser.parse_file_content(file_content,
                                                      sheet_name='test')
        self._verify()

    def _verify(self):
        for key in self.content:
            self.content[key] = list(self.content[key])
        eq_(self.content, {'test': [[1, 2, 3]]})


def get_file(file_name):
    return os.path.join("tests", "fixtures", file_name)
