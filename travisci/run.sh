#!/bin/bash

set -euv

# We can run the flake8 tests on py27 and above
if [ ${TRAVIS_PYTHON_VERSION:0:3} == 2.6 ]; then
  python setup.py test
else
  python setup.py test -a --flake8
fi
