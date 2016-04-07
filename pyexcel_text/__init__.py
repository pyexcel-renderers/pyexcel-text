"""
    pyexcel.ext.text
    ~~~~~~~~~~~~~~~~~~~

    Provide readable string prestation

    :copyright: (c) 2014 by C. W.
    :license: New BSD
"""
import json
from functools import partial

import tabulate

from pyexcel.sheets import NominableSheet, SheetStream
from pyexcel.sheets.matrix import uniform
from pyexcel.deprecated import deprecated
from pyexcel.sources import FileSource
from pyexcel.constants import KEYWORD_FILE_NAME


TABLEFMT = "simple"
_SHARED_MESSAGE = """
Deprecated since v0.0.3! Please use pyexcel's save_as, save_book_as
"""


def class_name(name):
    return "<class '%s'>" % name


def present_matrix(matrix_instance):
    """Textualize a Matrix"""
    if TABLEFMT == "json":
        return json.dumps(matrix_instance.to_array())
    else:
        return tabulate.tabulate(matrix_instance.to_array(), tablefmt=TABLEFMT)


def present_nominable_sheet(nmsheet_instance):
    """Textualize a NominableSheet"""
    if TABLEFMT == "json":
        return json.dumps({
            nmsheet_instance.name: nmsheet_instance.to_array()
        })
    else:
        ret = "Sheet Name: %s\n" % nmsheet_instance.name
        if len(nmsheet_instance.colnames) > 0:
            data = nmsheet_instance.to_array()
            return ret+tabulate.tabulate(data, headers="firstrow",
                                         tablefmt=TABLEFMT)
        else:
            return ret+present_matrix(nmsheet_instance)


def present_book(book_instance):
    """Textualize a pyexcel Book"""
    if TABLEFMT == "json":
        return json.dumps(book_instance.to_dict())
    else:
        ret = ""
        for sheet in book_instance.sheets:
            ret += present_nominable_sheet(book_instance.sheets[sheet])
            ret += "\n"
        return ret.strip('\n')


@partial(
    deprecated,
    message=(_SHARED_MESSAGE +
             " or instance method Sheet.save_as or Book.save_as"))
def save_as(instance, filename):
    """Save a pyexcel instance as text to a file"""
    with open(filename, "w") as outfile:
        outfile.write(str(instance))


@partial(
    deprecated,
    message=(
        _SHARED_MESSAGE +
        " or instance method Sheet.save_to_memory or Book.save_to_memory"
    )
)
def save_to_memory(instance, stream):
    """Save a pyexcel instance as text to a stream"""
    stream.write(str(instance))


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
        data = self.transform_data(sheet)
        with open(self.file_name, 'w') as textfile:
            self.write_sheet(textfile, data, sheet.name)

    def write_sheet(self, textfile, data, title):
        if self.write_title:
            textfile.write("Sheet Name: %s\n" % title)
        textfile.write(tabulate.tabulate(data,
                                         tablefmt=self.file_type,
                                         **self.keywords))
        textfile.write("\n")

    def transform_data(self, sheet):
        table = []
        if isinstance(sheet, SheetStream):
            table = list(sheet.to_array())
            width, table = uniform(table)

        if isinstance(sheet, NominableSheet):
            if len(sheet.colnames) > 0:
                self.keywords['headers'] = 'firstrow'
            table = sheet.to_array()
        return table


class TextBookSource(TextSheetSource):
    def write_data(self, book):
        with open(self.file_name, 'w') as textfile:
            self.write_book(textfile, book)

    def write_book(self, textfile, book):
        for sheet in book:
            data = self.transform_data(sheet)
            self.write_sheet(textfile, data, sheet.name)


class HtmlSheetSource(TextSheetSource):
    TEXT_FILE_FORMATS = ['html']

    def write_sheet(self, textfile, data, title):
        textfile.write("<html><header><title>%s</title><body>" % self.file_name)
        TextSheetSource.write_sheet(self, textfile, data, title)
        textfile.write("</body></html>")


class HtmlBookSource(TextBookSource):
    TEXT_FILE_FORMATS = ['html']

    def write_book(self, textfile, book):
        textfile.write("<html><header><title>%s</title><body>" % self.file_name)
        TextBookSource.write_book(self, textfile, book)
        textfile.write("</body></html>")


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

    def __init__(self, file_name=None, **keywords):
        self.file_name = file_name
        self.keywords = keywords

    def write_data(self, sheet):
        data = self.transform_data(sheet)
        with open(self.file_name, 'w') as jsonfile:
            jsonfile.write(json.dumps(data, sort_keys=True))

    def transform_data(self, sheet):
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


class JsonBookSource(JsonSheetSource):
    """
    Write a dictionary of two dimensional arrays into json format
    """
    def write_data(self, book):
        if self.keywords.get('single_sheet_in_book', False):
            keys = list(book.keys())
            JsonSheetSource.write_data(book[keys[0]])
        else:
            with open(self.file_name, 'w') as jsonfile:
                jsonfile.write(json.dumps(book.to_dict(), sort_keys=True))


def extend_sources(SourceFactory):
    SourceFactory.register_a_source("sheet", "write", JsonSheetSource)
    SourceFactory.register_a_source("book", "write", JsonBookSource)
    SourceFactory.register_a_source("sheet", "write", TextSheetSource)
    SourceFactory.register_a_source("book", "write", TextBookSource)
    SourceFactory.register_a_source("sheet", "write", HtmlSheetSource)
    SourceFactory.register_a_source("book", "write", HtmlBookSource)


def extend_presentation(presentation):
    presentation.update({
        class_name("pyexcel.sheets.matrix.Matrix"): present_matrix,
        class_name("pyexcel.sheets.matrix.FormattableSheet"): present_matrix,
        class_name("pyexcel.sheets.matrix.FilterableSheet"): present_matrix,
        class_name("pyexcel.sheets.sheet.NominableSheet"): present_nominable_sheet,
        class_name("pyexcel.sheets.sheet.Sheet"): present_nominable_sheet,
        class_name("pyexcel.book.Book"): present_book
    })
