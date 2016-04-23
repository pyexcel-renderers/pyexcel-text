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
    'html',
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
    """
    Write up all memory source initialization once here
    """
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
    Base class for all sources in this module
    """
    fields = [params.FILE_NAME]
    targets = (params.SHEET,)
    actions = (params.WRITE_ACTION,)
    text_file_formats = file_types

    @classmethod
    def can_i_handle(cls, action, file_type):
        status = False
        if action == params.WRITE_ACTION and file_type in cls.text_file_formats:
            status = True
        return status


class TextSheetSource(TextSource):
    """
    A single sheet in text format
    """
    def __init__(self, file_name=None, write_title=True, **keywords):
        self.file_name = file_name
        self.keywords = keywords
        self.write_title = write_title
        self.file_type = file_name.split(".")[-1]

    def write_data(self, sheet):
        """
        Call by pyexcel to write out a sheet instance
        """
        data = self._transform_data(sheet)
        with open(self.file_name, 'w') as textfile:
            self.write_sheet(textfile, data, sheet.name)

    def write_sheet(self, textfile, data, title):
        """write out data to a file handle

        the file handle can be a stream
        """
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
    """
    Write to an io stream
    """
    fields = [params.FILE_TYPE]

    def __init__(self, file_type=None, file_stream=None,
                 write_title=True, **keywords):
        WriteOnlyMemorySourceMixin.__init__(
            self, file_type=file_type,
            file_stream=file_stream, write_title=write_title, **keywords)

    def write_data(self, sheet):
        """no need to close file because it is a memory stream"""
        data = self._transform_data(sheet)
        self.write_sheet(self.content, data, sheet.name)


class TextBookSource(TextSheetSource):
    """
    A excel book in text format
    """
    targets = (params.BOOK,)

    def __init__(self, file_name=None, write_title=True, **keywords):
        self.file_name = file_name
        self.keywords = keywords
        self.write_title = write_title
        self.file_type = file_name.split(".")[-1]

    def write_data(self, book):
        """Override TextSheetSource.write_data so as to write a book"""
        with open(self.file_name, 'w') as textfile:
            self.write_book(textfile, book)

    def write_book(self, textfile, book):
        """but write_book in turn needs to write_sheet"""
        for sheet in book:
            data = self._transform_data(sheet)
            self.write_sheet(textfile, data, sheet.name)


class TextBookSourceInMemory(TextBookSource, WriteOnlyMemorySourceMixin):
    """
    Write book in text format to memory
    """
    fields = [params.FILE_TYPE]

    def __init__(self, file_type=None, file_stream=None,
                 write_title=True, **keywords):
        WriteOnlyMemorySourceMixin.__init__(
            self, file_type=file_type,
            file_stream=file_stream, write_title=write_title, **keywords)

    def write_data(self, book):
        """Yet again, no need to close a memory stream"""
        self.write_book(self.content, book)


# register sources
sources = (TextSheetSource, TextBookSource,
           TextSheetSourceInMemory, TextBookSourceInMemory)
