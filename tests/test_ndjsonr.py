import os
from nose.tools import eq_, raises
from pyexcel._compact import StringIO
from pyexcel_text.ndjsonr import NDJsonParser as JsonParser
from pyexcel_text.ndjsonr import ARRAY, RECORDS, DICT, AUTO_DETECT


class TestStructure:

    def setUp(self):
        self.parser = JsonParser("json")

    def test_dict(self):
        sheet_name = 'test'
        self.content = self.parser.parse_file(get_file("dict.ndjson"),
                                              struct=DICT,
                                              sheet_name=sheet_name)
        expected = {
            sheet_name: [
                [u'a', 1, 2],
                [u'b', 2, 3],
                [u'c', 4, 5]
            ]
        }
        self._verify(expected)

    def test_dict(self):
        sheet_name = 'test'
        self.content = self.parser.parse_file(get_file("dict.ndjson"),
                                              sheet_name=sheet_name)
        expected = {
            sheet_name: [
                [u'a', 1, 2],
                [u'b', 2, 3],
                [u'c', 4, 5]
            ]
        }
        self._verify(expected)

    def test_records(self):
        sheet_name = 'test'
        self.content = self.parser.parse_file(get_file("records.ndjson"),
                                              struct=RECORDS,
                                              sheet_name=sheet_name)
        expected = {
            sheet_name: [
                ['a', 'b', 'c'],
                [1, 2, 3],
                [1, 2, 4]
            ]
        }
        self._verify(expected)

    def test_auto_detect_records(self):
        sheet_name = 'test'
        self.content = self.parser.parse_file(get_file("records.ndjson"),
                                              struct=AUTO_DETECT,
                                              sheet_name=sheet_name)
        expected = {
            sheet_name: [
                ['a', 'b', 'c'],
                [1, 2, 3],
                [1, 2, 4]
            ]
        }
        self._verify(expected)

    @raises(Exception)
    def test_unknown(self):
        sheet_name = 'test'
        self.content = self.parser.parse_file(get_file("records.ndjson"),
                                              struct='unknown',
                                              sheet_name=sheet_name)

    def _verify(self, expected):
        for key in self.content:
            self.content[key] = list(self.content[key])
        eq_(self.content, expected)


class TestMedia:

    def setUp(self):
        self.parser = JsonParser("json")

    def test_file(self):
        self.content = self.parser.parse_file(get_file("array.ndjson"),
                                              on_demand=True,
                                              struct=ARRAY,
                                              sheet_name='test')
        self._verify()

    def test_file(self):
        self.content = self.parser.parse_file(get_file("array.ndjson"),
                                              on_demand=True,
                                              sheet_name='test')
        self._verify()

    def test_stream(self):
        with open(get_file("array.ndjson"), 'r') as f:
            file_stream = StringIO(f.read())
        self.content = self.parser.parse_file_stream(file_stream,
                                                     struct=ARRAY,
                                                     sheet_name='test')
        self._verify()

    def test_content(self):
        with open(get_file("array.ndjson"), 'r') as f:
            file_content = f.read()
        self.content = self.parser.parse_file_content(file_content,
                                                      struct=ARRAY,
                                                      sheet_name='test')
        self._verify()

    def _verify(self):
        for key in self.content:
            self.content[key] = list(self.content[key])
        eq_(self.content, {'test': [[1, 2, 3]]})


def get_file(file_name):
    return os.path.join("tests", "fixtures", file_name)
