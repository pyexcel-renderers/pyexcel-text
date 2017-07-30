"""
    pyexcel_text.ndjsonr
    ~~~~~~~~~~~~~~~~~~~~~~

    Render newline delimited json input

    :copyright: (c) 2014-2017 by C. W.
    :license: New BSD
"""
import json
import itertools
import pyexcel._compact as compact
import pyexcel.constants as constants
from pyexcel.parser import AbstractParser
from pyexcel.plugins.sources.pydata.common import (
    ArrayReader, RecordsReader)


AUTO_DETECT = 'AD'
ARRAY = 'A'
RECORDS = 'R'
DICT = 'D'


# pylint: disable=W0223
class FlatDictReader(ArrayReader):
    """read data from a dictionary via pyexcel-io interface"""

    def row_iterator(self):
        for row in self._native_sheet:
            for key, item in row.items():
                if isinstance(item, list):
                    yield [key] + item
                else:
                    yield [key, item]


READERS = {
    ARRAY: ArrayReader,
    RECORDS: RecordsReader,
    DICT: FlatDictReader
}


class NDJsonParser(AbstractParser):
    """
    parse ndjson
    """
    def parse_file(self, file_name, on_demand=False, **keywords):
        if on_demand:
            file_handle = open(file_name, 'r')
            content = self.parse_file_stream(file_handle, **keywords)
            self._free_me_up_later(file_handle)
            return content
        else:
            with open(file_name, 'r') as f:
                content = self.parse_file_stream(f, **keywords)
                for key in content:
                    content[key] = list(content[key])
                return content

    def parse_file_stream(self, file_stream, struct=AUTO_DETECT,
                          sheet_name=constants.DEFAULT_NAME,
                          **keywords):
        content = json_loads(file_stream)
        if struct == AUTO_DETECT:
            struct, content = detect_format(content)
            if struct == AUTO_DETECT:
                raise Exception(
                    "No auto detection is supported in this version")

        if struct in READERS:
            reader = READERS[struct](content, **keywords)
        else:
            raise Exception("Unknown data structure")
        return {sheet_name: reader.to_array()}

    def parse_file_content(self, file_content, **keywords):
        return self.parse_file_stream(
            compact.StringIO(file_content), **keywords)


def json_loads(file_stream):
    """
    Simple load each line as json
    """
    try:
        for raw_row in file_stream:
            yield json.loads(raw_row)
    except ValueError:
        raise ValueError("There has been an json decode error."
                         "Current version is not error tolerant")


def detect_format(content_generator):
    """
    This function need to make sheet.ndjson to work
    """
    struct = AUTO_DETECT
    first_line = next(content_generator)
    if isinstance(first_line, list):
        struct = ARRAY
    elif isinstance(first_line, dict):
        keys = list(first_line.keys())
        if len(keys) > 1:
            struct = RECORDS
        else:
            struct = DICT
    return struct, itertools.chain([first_line], content_generator)
