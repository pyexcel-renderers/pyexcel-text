"""
    pyexcel.ext.text
    ~~~~~~~~~~~~~~~~~~~

    Provide readable string presetation

    :copyright: (c) 2014 by C. W.
    :license: New BSD
"""

from . import text, json, html

_SHARED_MESSAGE = """
Removed since v0.1.2! Please use save_as, save_book_as of pyexcel or
pyexcel.Sheet.save_as, pyexcel.Book.save_as.
"""

sources = text.sources + json.sources + html.sources
file_types = text.file_types + json.file_types + html.file_types

def save_as(instance, filename):
    raise Exception(_SHARED_MESSAGE)


def save_to_memory(instance, stream):
    raise Exception(_SHARED_MESSAGE)
