"""
    pyexcel_text
    ~~~~~~~~~~~~~~~~~~~

    Provide text output

    :copyright: (c) 2014 by C. W.
    :license: New BSD
"""
from . import _text as text
from . import _json as json


_SHARED_MESSAGE = """
Removed since v0.1.2! Please use save_as, save_book_as of pyexcel or
pyexcel.Sheet.save_as, pyexcel.Book.save_as.
"""

sources = text.sources + json.sources
file_types = text.file_types + json.file_types


def save_as(instance, filename):
    """
    Legacy modular function. Now it is removed

    raising an exception here to get the attention of
    the user of pyexcel
    """
    raise Exception(_SHARED_MESSAGE)


def save_to_memory(instance, stream):
    """
    Legacy modular function. Now it is removed

    raising an exception here to get the attention of
    the user of pyexcel
    """
    raise Exception(_SHARED_MESSAGE)
