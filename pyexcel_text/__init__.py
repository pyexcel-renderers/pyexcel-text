"""
    pyexcel_text
    ~~~~~~~~~~~~~~~~~~~

    Provide text output

    :copyright: (c) 2014-2016 by C. W.
    :license: New BSD
"""
from pyexcel.internal.common import PyexcelPluginList


PyexcelPluginList(__name__).add_a_renderer(
    submodule='_text.Tabulater',
    file_types=[
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
    ],
    stream_type='string'
).add_a_renderer(
    submodule='_json.Jsonifier',
    file_types=['json'],
    stream_type='string'
)
