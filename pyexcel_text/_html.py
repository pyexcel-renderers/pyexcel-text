"""
    pyexcel_text.html
    ~~~~~~~~~~~~~~~~~~~

    Provide html output

    :copyright: (c) 2014-2016 by C. W.
    :license: New BSD
"""
from ._text import TextSheetSource, TextBookSource
from ._text import TextSheetSourceInMemory, TextBookSourceInMemory


file_types = ('html',)


class HtmlMixin(object):
    """provide html header and footer"""
    def write_html_header(self, open_filehandle, title):
        open_filehandle.write("<html><header><title>%s</title><body>" % title)

    def write_html_footer(self, open_filehandle):
        open_filehandle.write("</body></html>")


class HtmlSheetSource(TextSheetSource, HtmlMixin):
    text_file_formats = ['html']

    def write_sheet(self, textfile, data, title):
        self.write_html_header(textfile, self.file_name)
        TextSheetSource.write_sheet(self, textfile, data, title)
        self.write_html_footer(textfile)


class HtmlSheetSourceInMemory(TextSheetSourceInMemory, HtmlMixin):
    text_file_formats = ['html']

    def write_sheet(self, textfile, data, title):
        self.write_html_header(textfile, title)
        TextSheetSource.write_sheet(self, textfile, data, title)
        self.write_html_footer(textfile)


class HtmlBookSource(TextBookSource, HtmlMixin):
    text_file_formats = ['html']

    def write_book(self, textfile, book):
        self.write_html_header(textfile, self.file_name)
        TextBookSource.write_book(self, textfile, book)
        self.write_html_footer(textfile)


class HtmlBookSourceInMemory(TextBookSourceInMemory, HtmlMixin):
    text_file_formats = ['html']

    def write_book(self, textfile, book):
        self.write_html_header(textfile, "memory")
        TextBookSource.write_book(self, textfile, book)
        self.write_html_footer(textfile)


sources = (HtmlSheetSource, HtmlBookSource,
           HtmlBookSourceInMemory, HtmlSheetSourceInMemory)
