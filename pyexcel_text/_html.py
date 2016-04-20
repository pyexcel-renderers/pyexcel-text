from ._text import TextSheetSource, TextBookSource
from ._text import TextSheetSourceInMemory, TextBookSourceInMemory


file_types = ('html',)


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


sources = (HtmlSheetSource, HtmlBookSource, HtmlBookSourceInMemory, HtmlSheetSourceInMemory)
