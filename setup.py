"""
    pyexcel-text
    ~~~~~~~~~~~~~~

    textual plugin for pyexcel
"""

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

with open("README.rst", 'r') as readme:
    README_txt = readme.read()

with open("VERSION", "r") as version:
    version_txt = version.read().rstrip()

setup(
    name='pyexcel-text',
    author="C. W.",
    version=version_txt,
    author_email="wangc_2011@hotmail.com",
    url="https://github.com/chfw/pyexcel-text",
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    install_requires=[
        'pyexcel>=0.2.0',
        'pyexcel-io>=0.1.0',
        'tabulate'
    ],
    description="It is a plugin to pyexcel and provides the capbility to present and write data in text fromats",
    long_description=README_txt,
    tests_require=['nose'],
    zip_safe=False,
    license='New BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Office/Business',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)
