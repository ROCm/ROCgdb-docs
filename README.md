# ROCgdb-docs

Documentation repository for [ROCgdb](https://github.com/ROCm-Developer-Tools/ROCgdb)

## Important files from the submodule

The HTML files in the base GDB needs to be built.

The `build_docs.py` script handles this.

Simply update the submodule to the desired branch, then run the script.

```bash
# update submodule
cd ROCgdb
git fetch origin
git checkout <desired branch>
git pull
cd ..
# build the HTML docs for GDB
# and prepare them for hosting by Read the Docs
./build_docs.sh
```

## How to build documentation locally

Run the following steps to build the base documentation site:

```bash
cd docs
pip3 install -r sphinx/requirements.txt
python3 -m sphinx -T -E -b html -d _build/doctrees -D language=en . _build/html
```

Run the additional following steps to build the gdb documentation and display it locally with the documentation site:

```bash
cd ..
git submodule update --init --recursive
cd ROCgdb
./configure
make
make do-html
cd ..
cp -v --parents `find ROCgdb/ -name "*.html"` docs/_build/html
```

Alternatively, change `build_docs.sh` and run it.

Change:

```diff
- cp -v --parents `find ROCgdb/ -name '*.html'` _readthedocs/html
+ cp -v --parents `find ROCgdb/ -name '*.html'` docs/_build/html
```

Command:

```bash
./build_docs.sh
```
