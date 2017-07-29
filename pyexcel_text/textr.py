"""
    pyexcel_text.html
    ~~~~~~~~~~~~~~~~~~~

    Provide tabulate output, see file_types for more details

    :copyright: (c) 2014-2016 by C. W.
    :license: New BSD
"""
import tabulate

from pyexcel.internal import SheetStream
from pyexcel.internal.sheets.matrix import uniform
from pyexcel.renderer import Renderer


class Tabulater(Renderer):
    def render_sheet(self, sheet):
        content = tabulating(sheet, self._file_type, self._write_title)
        self._stream.write(content)


def tabulating(sheet, file_type, write_title):
    content = ""
    if write_title:
        content += "%s:\n" % sheet.name
    table = []
    keywords = {}
    if isinstance(sheet, SheetStream):
        table = list(sheet.to_array())
        width, table = uniform(table)
    else:
        if len(sheet.colnames) > 0:
            keywords['headers'] = 'firstrow'
        table = sheet.to_array()
    content += tabulate.tabulate(
        table,
        tablefmt=file_type,
        **keywords)
    return content
