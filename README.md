# ROCgdb-docs

Documentation repository for [ROCgdb](https://github.com/ROCm-Developer-Tools/ROCgdb)

## How to build documentation locally

Run the following steps to build the base documentation site:

```
cd docs
pip3 install -r .sphinx/requirements.txt
python3 -m sphinx -T -E -b html -d _build/doctrees -D language=en . _build/html
```

Run the additional following steps to build the gdb documentation:

```
cd ..
git submodule update --init --recursive
git submodule update --remote --merge
cd ROCgdb
./configure
make do-html
cd ..
cp -v --parents `find ROCgdb/ -name "*.html"` docs/_build/html
```

## How to update documentation on Read the Docs

Run `build_docs.py` and push the changes made to ROCgdb-docs (not the ROCgdb submodule)
