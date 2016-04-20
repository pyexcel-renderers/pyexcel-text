import json

from pyexcel.book import Book
from pyexcel.sheets import Sheet
from pyexcel.sources import FileSource, SourceFactory
from pyexcel.constants import KEYWORD_FILE_NAME, KEYWORD_FILE_TYPE

from ._compact import StringIO


class JsonSource(FileSource):
    """
    Write into json file
    """
    @classmethod
    def can_i_handle(cls, action, file_type):
        status = False
        if action == 'write' and file_type == "json":
            status = True
        return status


class JsonSheetSource(JsonSource):
    """
    Write a two dimensional array into json format
    """
    fields = [KEYWORD_FILE_NAME]

    def __init__(self, file_name=None, write_title=True, **keywords):
        self.file_name = file_name
        self.write_title = write_title
        self.keywords = keywords

    def write_data(self, sheet):
        data = self._transform_data(sheet)
        with open(self.file_name, 'w') as jsonfile:
            if self.write_title:
                data = {sheet.name: data}
            self._write_sheet(jsonfile, data)

    def _write_sheet(self, jsonfile, data):
        jsonfile.write(json.dumps(data, sort_keys=True))

    def _transform_data(self, sheet):
        table = sheet.to_array()
        if hasattr(sheet, 'colnames'):
            colnames = sheet.colnames
            rownames = sheet.rownames
            # In the following, row[0] is the name of each row
            if colnames and rownames:
                table = dict((row[0], dict(zip(colnames, row[1:])))
                             for row in table[1:])
            elif colnames:
                table = [dict(zip(colnames, row)) for row in table[1:]]
            elif rownames:
                table = dict((row[0], row[1:]) for row in table)
        else:
            table = list(table)
        return table


class JsonSheetSourceInMemory(JsonSheetSource):
    fields = [KEYWORD_FILE_TYPE]
    def __init__(self, file_type=None, file_stream=None, write_title=True,
                 **keywords):
        if file_stream:
            self.content = file_stream
        else:
            self.content = StringIO()
        self.file_type = file_type
        self.write_title = write_title
        self.keywords = keywords

    def write_data(self, sheet):
        data = self._transform_data(sheet)
        if self.write_title:
            data = {sheet.name: data}
        self._write_sheet(self.content, data)


def write_json_book(jsonfile, bookdict):
    jsonfile.write(json.dumps(bookdict, sort_keys=True))


class JsonBookSourceInMemory(JsonSheetSourceInMemory):

    def write_data(self, book):
        write_json_book(self.content, book.to_dict())

        
class JsonBookSource(JsonSheetSource):
    """
    Write a dictionary of two dimensional arrays into json format
    """
    def write_data(self, book):
        with open(self.file_name, 'w') as jsonfile:
            write_json_book(jsonfile, book.to_dict())


SourceFactory.register_a_source("sheet", "write", JsonSheetSource)
SourceFactory.register_a_source("book", "write", JsonBookSource)
SourceFactory.register_a_source("sheet", "write", JsonSheetSourceInMemory)
SourceFactory.register_a_source("book", "write", JsonBookSourceInMemory)

Sheet.register_presentation('json')
Book.register_presentation('json')
