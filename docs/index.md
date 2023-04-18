AMD ROCm Debugger (ROCgdb)
==========================

Introduction
------------

The AMD ROCm Debugger (ROCgdb) is the AMD source-level debugger for Linux,
based on the GNU Debugger (GDB).  It enables heterogeneous debugging on the AMD
ROCm platform comprising of an x86-based host architecture along with
commercially available AMD GPU architectures supported by the AMD Debugger API
Library (ROCdbgapi).  The AMD Debugger API Library (ROCdbgapi) is included with
the AMD ROCm release.

The current AMD ROCm Debugger (ROCgdb) is an initial prototype that focuses on
source line debugging.  Symbolic variable debugging capabilities are not
currently supported.

For more information about AMD ROCm, see:

- https://rocmdocs.amd.com/

You can use the standard GDB commands for both CPU and GPU code debugging.  For
more information about ROCgdb, refer to the *ROCgdb User Guide* which is
installed at:

- ``/opt/rocm/share/info/gdb.info`` as a texinfo file
- ``/opt/rocm/share/doc/gdb/gdb.pdf`` as a PDF file

You can refer to the following chapters in the *ROCgdb User Guide* for more
specific information about debugging heterogeneous programs on AMD ROCm:

- *Debugging Heterogeneous Programs* provides general information about
  debugging heterogeneous programs.  It presents features and commands that are
  not currently implemented but provisionally planned for future versions.
- *Configuration-Specific Information > Architectures > AMD GPU* provides
  specific information about debugging heterogeneous programs on AMD ROCm with
  supported AMD GPU chips.  This section also lists the implementation status
  and known issues of the current version.

For more information about the GNU Debugger (GDB), refer to the ``README`` file
in this folder or check the GNU Debugger (GDB) web site at:

- http://www.gnu.org/software/gdb
