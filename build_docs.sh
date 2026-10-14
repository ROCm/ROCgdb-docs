#!/bin/bash

# Script to build the raw html ROCgdb documents from the source repository.
# Optionally, also generate the ROCgdb-docs documentation with Sphinx.

set -e

rm -rf _build
mkdir _build
pushd _build
# Only ROCgdb's own manuals are published, so do not configure the sibling
# binutils components. This drops their manuals from the output (as, binutils,
# gprof, gprofng, ld, ldint) - nothing in docs/ links to them - and is the single
# biggest saving left in this build.
../ROCgdb/configure --with-bugurl="https://github.com/ROCm/ROCgdb/issues" \
  --disable-binutils --disable-gas --disable-ld --disable-gold \
  --disable-gprof --disable-gprofng --disable-sim --disable-gdbserver

# No `make` here on purpose: do-html and do-pdf configure and build their own
# prerequisites, so compiling first only moves the work around. Measured on
# 16 CPUs against the same ROCgdb commit:
#
#   make (serial, as this script once did)        ~13 min   1956 html, 17 pdf
#   make -j16 + doc targets                        194s     1956 html, 17 pdf
#   make all-gdb -j16 + doc targets                169s     1956 html, 17 pdf
#   doc targets only                               151s     1956 html, 17 pdf
#   doc targets only, with the --disable-* above   109s     1122 html, 11 pdf
#
# Do not pass -j to do-html/do-pdf. The top-level recursion is not parallel-safe:
# it races a subdirectory's manual against that subdirectory's own configure and
# dies with "Error 1", leaving 23 of 1956 HTML files behind.

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