from nose.tools import raises
from pyexcel_text import save_as, save_to_memory



@raises(Exception)
def test_save_as():
    save_as("ainstance", "some file name")


@raises(Exception)
def test_save_to_memory():
    save_to_memory("ainstace", "astream")