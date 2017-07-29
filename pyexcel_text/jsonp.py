"""
    pyexcel_text.jsonp
    ~~~~~~~~~~~~~~~~~~~

    Parse json input

    :copyright: (c) 2014-2017 by C. W.
    :license: New BSD
"""
import json
import pyexcel.constants as constants
from pyexcel.parser import AbstractParser
from pyexcel.plugins.sources.pydata.common import (
    ArrayReader, RecordsReader, DictReader)
from pyexcel.plugins.sources.pydata.bookdict import BookDictSource


class JsonParser(AbstractParser):
    def parse_file(self, file_name, **keywords):
        with open(file_name, 'r') as f:
            content = json.load(f)
            return as_a_dict_of_2_dimensional_array(content, **keywords)

    def parse_file_stream(self, file_stream, **keywords):
        content = json.load(file_stream)
        return as_a_dict_of_2_dimensional_array(content, **keywords)

    def parse_file_content(self, file_content, **keywords):
        content = json.loads(file_content)
        return as_a_dict_of_2_dimensional_array(content, **keywords)


def as_a_dict_of_2_dimensional_array(
        content, sheet_name=constants.DEFAULT_NAME,
        **keywords):
    if isinstance(content, list):
        if isinstance(content[0], list):
            array_reader = ArrayReader(content, **keywords)
            return {sheet_name: array_reader.to_array()}
        elif isinstance(content[0], dict):
            records_reader = RecordsReader(content, **keywords)
            return {sheet_name: records_reader.to_array()}
        else:
            raise ValueError("Unknow file format")
    elif isinstance(content, dict):
        try:
            keys = list(content.keys())
            first_item = content.get(keys[0])[0]
        except Exception as e:
            print(e)
            raise
        if isinstance(first_item, list):
            bookdict = BookDictSource(content, **keywords)
            return bookdict.get_data()
        else:
            dict_reader = DictReader(content, **keywords)
            return {sheet_name: dict_reader.to_array()}
