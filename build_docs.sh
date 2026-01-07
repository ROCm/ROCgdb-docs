#!/bin/bash

# Script to build the raw html ROCgdb documents from the source repository.
# Optionally, also generate the ROCgdb-docs documentation with Sphinx.

set -e

git submodule update --init --recursive
cd ROCgdb
./configure
make
make do-html
cd ..
mkdir --parents _readthedocs/html
cp -v --parents `find ROCgdb/ -name '*.html'` _readthedocs/html

# OPTIONAL: also generate the ROCgdb-docs documentation
# cd docs
# pip3 install -r sphinx/requirements.txt
# python3 -m sphinx -T -E -b html -d _build/doctrees -D language=en . _build/html
