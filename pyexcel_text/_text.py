"""
    pyexcel_text.html
    ~~~~~~~~~~~~~~~~~~~

    Provide tabulate output, see file_types for more details

    :copyright: (c) 2014-2016 by C. W.
    :license: New BSD
"""
import tabulate

from pyexcel.sheets import NominableSheet, SheetStream
from pyexcel.sheets.matrix import uniform


file_types = (
    'html',
    'simple',
    'plain',
    'grid',
    'pipe',
    'orgtbl',
    'rst',
    'mediawiki',
    'latex',
    'latex_booktabs'
)

def tabulating(sheet, file_type, write_title):
    content = ""
    if write_title:
        content += "%s:\n" % sheet.name
    table = []
    keywords = {} 
    if isinstance(sheet, SheetStream):
        table = list(sheet.to_array())
        width, table = uniform(table)

    if isinstance(sheet, NominableSheet):
        if len(sheet.colnames) > 0:
            keywords['headers'] = 'firstrow'
        table = sheet.to_array()
    content += tabulate.tabulate(
        table,
        tablefmt=file_type,
        **keywords)
    return content


renderer = (tabulating, None)