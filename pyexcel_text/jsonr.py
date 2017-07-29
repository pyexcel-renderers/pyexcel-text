"""
    pyexcel_text.json
    ~~~~~~~~~~~~~~~~~~~

    Provide json output

    :copyright: (c) 2014-2016 by C. W.
    :license: New BSD
"""
import json
import datetime
from pyexcel.renderer import Renderer


class Jsonifier(Renderer):

    def render_sheet(self, sheet):
        content = jsonify(sheet, self._file_type, self._write_title)
        self._stream.write(content)

    def render_book(self, book):
        content = jsonify_book(book, self._file_type)
        self._stream.write(content)


def jsonify(sheet, file_type, write_title):
    content = ""
    table = sheet.to_array()
    if hasattr(sheet, 'rownames'):
        colnames = sheet.colnames
        rownames = sheet.rownames
        # In the following, row[0] is the name of each row
        if colnames and rownames:
            table = dict((row[0], dict(zip(colnames, row[1:])))
                         for row in table[1:])
        elif colnames:
            table = sheet.to_records()
        elif rownames:
            table = sheet.to_records()
    else:
        table = list(table)
    if write_title:
        content = {sheet.name: table}
    else:
        content = table
    return json.dumps(content, sort_keys=True, default=_serializer)


def jsonify_book(book, file_type):
    return json.dumps(book.to_dict(), sort_keys=True,
                      default=_serializer)


def _serializer(obj):
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S.%f')
    elif isinstance(obj, datetime.date):
        return obj.strftime('%Y-%m-%d')
    return str(obj)
