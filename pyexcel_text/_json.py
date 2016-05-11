"""
    pyexcel_text.json
    ~~~~~~~~~~~~~~~~~~~

    Provide json output

    :copyright: (c) 2014-2016 by C. W.
    :license: New BSD
"""
import json


file_types = ('json',)


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


renderer = (jsonify, jsonify_book)
