from pyexcel.book import Book
from pyexcel.sheets import Sheet
from pyexcel.sources import SourceFactory

from .text import TextSheetSource, TextBookSource
from .text import TextSheetSourceInMemory, TextBookSourceInMemory


class HtmlMixin(object):
    def write_html_header(self, open_filehandle, title):
        open_filehandle.write("<html><header><title>%s</title><body>" % title)

    def write_html_footer(self, open_filehandle):
        open_filehandle.write("</body></html>")


class HtmlSheetSource(TextSheetSource, HtmlMixin):
    TEXT_FILE_FORMATS = ['html']

    def _write_sheet(self, textfile, data, title):
        self.write_html_header(textfile, self.file_name)
        TextSheetSource._write_sheet(self, textfile, data, title)
        self.write_html_footer(textfile)


class HtmlSheetSourceInMemory(TextSheetSourceInMemory, HtmlMixin):
    TEXT_FILE_FORMATS = ['html']

    def _write_sheet(self, textfile, data, title):
        self.write_html_header(textfile, "memory")
        TextSheetSource._write_sheet(self, textfile, data, title)
        self.write_html_footer(textfile)


class HtmlBookSource(TextBookSource, HtmlMixin):
    TEXT_FILE_FORMATS = ['html']

    def _write_book(self, textfile, book):
        self.write_html_header(textfile, self.file_name)
        TextBookSource._write_book(self, textfile, book)
        self.write_html_footer(textfile)


class HtmlBookSourceInMemory(TextBookSourceInMemory, HtmlMixin):
    TEXT_FILE_FORMATS = ['html']

    def _write_book(self, textfile, book):
        self.write_html_header(textfile, "memory")
        TextBookSource._write_book(self, textfile, book)
        self.write_html_footer(textfile)


SourceFactory.register_a_source("sheet", "write", HtmlSheetSource)
SourceFactory.register_a_source("book", "write", HtmlBookSource)
SourceFactory.register_a_source("sheet", "write", HtmlSheetSourceInMemory)
SourceFactory.register_a_source("book", "write", HtmlBookSourceInMemory)

Sheet.register_presentation('html')
Book.register_presentation('html')
