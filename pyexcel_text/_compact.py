"""
    pyexcel_text._compact
    ~~~~~~~~~~~~~~~~~~~

    provide cross python compatibility

    :copyright: (c) 2014-2016 by C. W.
    :license: New BSD
"""
import sys

if sys.version_info[0] == 2:
    from StringIO import StringIO
else:
    from io import StringIO

