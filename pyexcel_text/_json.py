"""
    pyexcel_text.json
    ~~~~~~~~~~~~~~~~~~~

    Provide json output

    :copyright: (c) 2014-2016 by C. W.
    :license: New BSD
"""
import json
from pyexcel.sources.renderer import Renderer

file_types = ('json',)


class Jsonifier(Renderer):
    file_types = ('json',)

    def render_sheet(self, sheet):
        content = jsonify(sheet, self.file_type, self.write_title)
        self.stream.write(content)

    def render_book(self, book):
        content = jsonify_book(book, self.file_type)
        self.stream.write(content)

        
def jsonify(sheet, file_type, write_title):
    content = ""
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
    if write_title:
        content = {sheet.name: table}
    else:
        content = table
    return json.dumps(content, sort_keys=True)


def jsonify_book(book, file_type):
    return json.dumps(book.to_dict(), sort_keys=True)


renderer = (Jsonifier,)
