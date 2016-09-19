"""
    pyexcel_text
    ~~~~~~~~~~~~~~~~~~~

    Provide text output

    :copyright: (c) 2014-2016 by C. W.
    :license: New BSD
"""
from . import _text  # noqa
from . import _json  # noqa


_SHARED_MESSAGE = """
Removed since v0.1.2! Please use save_as, save_book_as of pyexcel or
pyexcel.Sheet.save_as, pyexcel.Book.save_as.
"""


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
