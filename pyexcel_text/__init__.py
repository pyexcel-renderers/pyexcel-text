"""
    pyexcel_text
    ~~~~~~~~~~~~~~~~~~~

    Provide text output

    :copyright: (c) 2014-2016 by C. W.
    :license: New BSD
"""
__TEXT_META__ = {
    'plugin_type': 'renderer',
    'submodule': '_text',
    'file_types': [
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
    'stream_type': 'string'
}

__JSON_META__ = {
    'plugin_type': 'renderer',
    'submodule': '_json',
    'file_types': ['json'],
    'stream_type': 'string'
}

__pyexcel_plugins__ = [
    __TEXT_META__,
    __JSON_META__
]
