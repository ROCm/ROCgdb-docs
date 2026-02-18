#!/bin/bash

# Script to build the raw html ROCgdb documents from the source repository.
# Optionally, also generate the ROCgdb-docs documentation with Sphinx.

set -e

rm -rf _build
mkdir _build
pushd _build
../ROCgdb/configure
make

# Generate HTML
make do-html

# Generate pdf
make do-pdf

popd

# Copy HTML output for ReadTheDocs
rm -rf _readthedocs/html
mkdir --parents _readthedocs/html/ROCgdb
pushd _build
cp -v --parents `find . -name '*.html'` ../_readthedocs/html/ROCgdb
popd

# Copy generated PDFs to docs/_static/pdf
rm -rf docs/_static/pdf
mkdir --parents docs/_static/pdf/ROCgdb
pushd _build
find . -name '*.pdf' -exec cp -v {} ../docs/_static/pdf/ROCgdb \;
popd

# OPTIONAL: also generate the ROCgdb-docs documentation
# cd docs
# pip3 install -r sphinx/requirements.txt
# python3 -m sphinx -T -E -b html -d _build/doctrees -D language=en . _build/html
# python3 -m sphinx -T -E -b latex -d _build/doctrees -D language=en . _build/latex
# make -C _build/latex