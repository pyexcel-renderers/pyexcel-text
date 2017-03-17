pip freeze
nosetests --with-cov --cover-package pyexcel_text --cover-package tests --with-doctest --doctest-extension=.rst README.rst tests  pyexcel_text && flake8 . --exclude=.moban.d --builtins=unicode,xrange,long
