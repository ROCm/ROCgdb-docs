"""
Script to build the raw html ROCgdb documents from the source repository.
Optionally, also generate the ROCgdb-docs documentation with Sphinx.
"""

import os

os.system("git submodule update --init --recursive")
os.system("git submodule update --remote --merge")
os.chdir("ROCgdb")
os.system("./configure")
os.system("make")
os.system("make do-html")
os.chdir("..")
os.system("mkdir --parents _readthedocs/html")
os.system("cp -v --parents `find ROCgdb/ -name '*.html'` _readthedocs/html")

# OPTIONAL: also generate the ROCgdb-docs documentation
# os.chdir("docs")
# os.system("pip3 install -r sphinx/requirements.txt")
# os.system("python3 -m sphinx -T -E -b html -d _build/doctrees -D language=en . _build/html")
