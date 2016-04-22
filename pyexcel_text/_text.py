"""
    pyexcel_text.html
    ~~~~~~~~~~~~~~~~~~~

    Provide tabulate output, see file_types for more details

    :copyright: (c) 2014-2016 by C. W.
    :license: New BSD
"""
import tabulate

from pyexcel.sheets import NominableSheet, SheetStream
from pyexcel.sheets.matrix import uniform
from pyexcel.sources.base import FileSource
from pyexcel.sources import params

from ._compact import StringIO


file_types = (
    'simple',
    'plain',
    'grid',
    'pipe',
    'orgtbl',
    'rst',
    'mediawiki',
    'latex',
    'latex_booktabs'
)

class WriteOnlyMemorySourceMixin(object):
    def __init__(self, file_type=None, file_stream=None, write_title=True,
                 **keywords):
        if file_stream:
            self.content = file_stream
        else:
            self.content = StringIO()
        self.file_type = file_type
        self.keywords = keywords
        self.write_title = write_title


class TextSource(FileSource):
    """
    Write into json file
    """
    TEXT_FILE_FORMATS = file_types
    @classmethod
    def can_i_handle(cls, action, file_type):
        status = False
        if action == params.WRITE_ACTION and file_type in cls.TEXT_FILE_FORMATS:
            status = True
        return status


class TextSheetSource(TextSource):
    fields = [params.FILE_NAME]
    targets = (params.SHEET,)
    actions = (params.WRITE_ACTION,)

    def __init__(self, file_name=None, write_title=True, **keywords):
        self.file_name = file_name
        self.keywords = keywords
        self.write_title = write_title
        self.file_type = file_name.split(".")[-1]

    def write_data(self, sheet):
        data = self._transform_data(sheet)
        with open(self.file_name, 'w') as textfile:
            self._write_sheet(textfile, data, sheet.name)

    def _write_sheet(self, textfile, data, title):
        if self.write_title:
            textfile.write("Sheet Name: %s\n" % title)
        textfile.write(tabulate.tabulate(data,
                                         tablefmt=self.file_type,
                                         **self.keywords))
        textfile.write("\n")

    def _transform_data(self, sheet):
        table = []
        if isinstance(sheet, SheetStream):
            table = list(sheet.to_array())
            width, table = uniform(table)

        if isinstance(sheet, NominableSheet):
            if len(sheet.colnames) > 0:
                self.keywords['headers'] = 'firstrow'
            table = sheet.to_array()
        return table


class TextSheetSourceInMemory(TextSheetSource, WriteOnlyMemorySourceMixin):
    fields = [params.FILE_TYPE]

    def __init__(self, file_type=None, file_stream=None,
                 write_title=True, **keywords):
        WriteOnlyMemorySourceMixin.__init__(
            self, file_type=file_type,
            file_stream=file_stream, write_title=write_title, **keywords)

    def write_data(self, sheet):
        data = self._transform_data(sheet)
        self._write_sheet(self.content, data, sheet.name)


class TextBookSource(TextSheetSource):
    targets = (params.BOOK,)

    def __init__(self, file_name=None, write_title=True, **keywords):
        self.file_name = file_name
        self.keywords = keywords
        self.write_title = write_title
        self.file_type = file_name.split(".")[-1]

    def write_data(self, book):
        with open(self.file_name, 'w') as textfile:
            self._write_book(textfile, book)

    def _write_book(self, textfile, book):
        for sheet in book:
            data = self._transform_data(sheet)
            self._write_sheet(textfile, data, sheet.name)


class TextBookSourceInMemory(TextBookSource, WriteOnlyMemorySourceMixin):
    fields = [params.FILE_TYPE]

    def __init__(self, file_type=None, file_stream=None,
                 write_title=True, **keywords):
        WriteOnlyMemorySourceMixin.__init__(
            self, file_type=file_type,
            file_stream=file_stream, write_title=write_title, **keywords)
            
    def write_data(self, book):
        self._write_book(self.content, book)


sources = (TextSheetSource, TextBookSource,
           TextSheetSourceInMemory, TextBookSourceInMemory)

