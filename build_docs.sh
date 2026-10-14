#!/bin/bash

# Script to build the raw html ROCgdb documents from the source repository.
# Optionally, also generate the ROCgdb-docs documentation with Sphinx.

set -e

rm -rf _build
mkdir _build
pushd _build
../ROCgdb/configure --with-bugurl="https://github.com/ROCm/ROCgdb/issues"

# Build only what the manuals need, in parallel. Measured on 16 CPUs against the
# same ROCgdb commit, all producing an identical 1956 HTML files + 17 PDFs:
# a full serial `make` (what this script used to do) ~13 min, `make -j16` 194s,
# `make all-gdb -j16` 169s.
make all-gdb -j"$(nproc)"

# Do not pass -j to do-html/do-pdf below. The top-level recursion is not
# parallel-safe: it races a subdirectory's manual against that subdirectory's own
# configure and dies with "Error 1", leaving 23 of 1956 HTML files behind.

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