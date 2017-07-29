"""
    pyexcel_text
    ~~~~~~~~~~~~~~~~~~~

    Provide text output

    :copyright: (c) 2014-2016 by C. W.
    :license: New BSD
"""
from pyexcel.plugins import PyexcelPluginChain


PyexcelPluginChain(__name__).add_a_renderer(
    relative_plugin_class_path='textr.Tabulater',
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
    relative_plugin_class_path='jsonr.Jsonifier',
    file_types=['json'],
    stream_type='string'
).add_a_parser(
    relative_plugin_class_path='jsonp.JsonParser',
    file_types=[
        'json'
    ]
).add_a_parser(
    relative_plugin_class_path='ndjsonp.NDJsonParser',
    file_types=[
        'ndjson'
    ]
)
