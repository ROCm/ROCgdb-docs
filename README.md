# ROCgdb-docs

Documentation repository for [ROCgdb](https://github.com/ROCm-Developer-Tools/ROCgdb)

## How to build documentation locally

Run the following steps to build the base documentation site:

```
cd docs
pip3 install -r .sphinx/requirements.txt
python3 -m sphinx -T -E -b html -d _build/doctrees -D language=en . _build/html
```

Run the additional following steps to build the gdb documentation and display it locally with the documentation site:

```
cd ..
git submodule update --init --recursive
git submodule update --remote --merge
cd ROCgdb
./configure
make
make do-html
cd ..
cp -v --parents `find ROCgdb/ -name "*.html"` docs/_build/html
```

Alternatively, change `build_docs.py` and run it.

Change:

```
- os.system("cp -v --parents `find ROCgdb/ -name '*.html'` _readthedocs/html")
+ os.system("cp -v --parents `find ROCgdb/ -name '*.html'` docs/_build/html")
```

Command:
```
python3 build_docs.py
```

## How to update documentation on Read the Docs

Run `build_docs.py` and push the changes in the `_readthedocs` folder.
