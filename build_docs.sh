#!/bin/bash

# Script to build the raw html ROCgdb documents from the source repository.
# Optionally, also generate the ROCgdb-docs documentation with Sphinx.

set -e

git submodule update --init --recursive
rm -rf _build
mkdir _build
pushd _build
../ROCgdb/configure
make
make do-html
popd
rm -rf _readthedocs/html
mkdir --parents _readthedocs/html/ROCgdb
pushd _build
cp -v --parents `find . -name '*.html'` ../_readthedocs/html/ROCgdb
popd

# OPTIONAL: also generate the ROCgdb-docs documentation
# cd docs
# pip3 install -r sphinx/requirements.txt
# python3 -m sphinx -T -E -b html -d _build/doctrees -D language=en . _build/html
