import tabulate

from pyexcel.book import Book
from pyexcel.sheets import NominableSheet, SheetStream, Sheet
from pyexcel.sheets.matrix import uniform
from pyexcel.sources import FileSource, SourceFactory
from pyexcel.constants import KEYWORD_FILE_NAME, KEYWORD_FILE_TYPE

from ._compact import StringIO


class TextSource(FileSource):
    """
    Write into json file
    """
    TEXT_FILE_FORMATS = [
        "simple",
        "plain",
        "grid",
        "pipe",
        "orgtbl",
        "rst",
        "mediawiki",
        "latex",
        "latex_booktabs"
    ]
    @classmethod
    def can_i_handle(cls, action, file_type):
        status = False
        if action == 'write' and file_type in cls.TEXT_FILE_FORMATS:
            status = True
        return status


class TextSheetSource(TextSource):
    fields = [KEYWORD_FILE_NAME]

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


class TextSheetSourceInMemory(TextSheetSource):
    fields = [KEYWORD_FILE_TYPE]

    def __init__(self, file_type=None, file_stream=None, write_title=True,
                 **keywords):
        if file_stream:
            self.content = file_stream
        else:
            self.content = StringIO()
        self.write_title=write_title
        self.file_type = file_type
        self.keywords = keywords
            
    def write_data(self, sheet):
        data = self._transform_data(sheet)
        self._write_sheet(self.content, data, sheet.name)


class TextBookSource(TextSheetSource):
    def write_data(self, book):
        with open(self.file_name, 'w') as textfile:
            self._write_book(textfile, book)

    def _write_book(self, textfile, book):
        for sheet in book:
            data = self._transform_data(sheet)
            self._write_sheet(textfile, data, sheet.name)


class TextBookSourceInMemory(TextBookSource):
    fields = [KEYWORD_FILE_TYPE]

    def __init__(self, file_type=None, file_stream=None, write_title=True, **keywords):
        if file_stream:
            self.content = file_stream
        else:
            self.content = StringIO()
        self.file_type = file_type
        self.write_title = write_title
        self.keywords = keywords
            
    def write_data(self, book):
        self._write_book(self.content, book)


SourceFactory.register_a_source("sheet", "write", TextSheetSource)
SourceFactory.register_a_source("book", "write", TextBookSource)
SourceFactory.register_a_source("sheet", "write", TextSheetSourceInMemory)
SourceFactory.register_a_source("book", "write", TextBookSourceInMemory)


Sheet.register_presentation('simple')
Sheet.register_presentation('plain')
Sheet.register_presentation("grid")
Sheet.register_presentation("pipe")
Sheet.register_presentation("orgtbl")
Sheet.register_presentation("rst")
Sheet.register_presentation("mediawiki")
Sheet.register_presentation("latex")
Sheet.register_presentation("latex_booktabs")
Book.register_presentation('simple')
Book.register_presentation('plain')
Book.register_presentation("grid")
Book.register_presentation("pipe")
Book.register_presentation("orgtbl")
Book.register_presentation("rst")
Book.register_presentation("mediawiki")
Book.register_presentation("latex")
Book.register_presentation("latex_booktabs")
