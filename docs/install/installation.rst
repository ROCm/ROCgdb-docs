.. meta::
   :description: Source-level debugger for Linux, based on the GNU Debugger
   :keywords: ROCgdb, ROCm, library, API, tool

.. _installation:

==============
Installation
==============

This document provides information required to build and install ROCm debugger.

Prerequisites
---------------

- A system supporting ROCm. See the `supported operating systems <https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-operating-systems>`_.

- A C++11 compiler such as GCC 4.8 or Clang 3.3.

- AMD Debugger API Library (ROCdbgapi) that can be installed as part of the
  ROCm release using the ``rocm-dbgapi`` package.

- Install the required packages according to the OS.

  - For Ubuntu 18.04 and Ubuntu 20.04:

    .. code-block:: bash

      apt install bison flex gcc make ncurses-dev texinfo g++ zlib1g-dev \
      libexpat-dev python3-dev liblzma-dev libgmp-dev libbabeltrace-dev \
      libbabeltrace-ctf-dev libmpfr-dev
  
  - For CentOS 8.1 and RHEL 8.1:

    .. code-block:: bash
    
      yum install -y epel-release centos-release-scl bison flex gcc make \
      texinfo texinfo-tex gcc-c++ zlib-devel expat-devel python3-devel \
      xz-devel gmp-devel libbabeltrace-devel ncurses-devel mpfr-devel
      wget http://repo.okay.com.mx/centos/8/x86_64/release/libbabeltrace-devel-1.5.4-2.el8.x86_64.rpm \
      && rpm -ivh --nodeps libbabeltrace-devel-1.5.4-2.el8.x86_64.rpm
  
  - For SLES 15 Service Pack 1:

    .. code-block:: bash

      zypper in bison flex gcc make texinfo gcc-c++ zlib-devel libexpat-devel \
      python3-devel xz-devel gmp-devel babeltrace-devel ncurses-devel mpfr-devel
  
Build 
---------

An example command-line to build ROCgdb on Linux:

.. code-block:: bash

  cd rocgdb
  mkdir build
  cd build
  ../configure --program-prefix=roc \
    --enable-64-bit-bfd --enable-targets="x86_64-linux-gnu,amdgcn-amd-amdhsa" \
    --disable-ld --disable-gas --disable-gdbserver --disable-sim --enable-tui \
    --disable-gdbtk --disable-gprofng --disable-shared --with-expat \
    --with-system-zlib --without-guile --with-babeltrace --with-lzma \
    --with-python=python3
  make

If ROCdbgapi is not installed in the system default location, specify ``PKG_CONFIG_PATH`` to make the correct build configuration available to ``pkg-config``.
If ROCdbgapi is installed in ``/opt/rocm-$ROCM_VERSION`` (default for ROCm packages), use ``PKG_CONFIG_PATH=/opt/rocm-$ROCM_VERSION/share/pkgconfig``.

If the system's dynamic linker is not configured to locate ROCdbgapi where it is
installed, ROCgdb can be configured and built using ``LDFLAGS="-Wl,-rpath=/opt/rocm-$ROCM_VERSION/lib"``. Alternatively, you can use
``LD_LIBRARY_PATH`` at runtime to indicate where ROCdbgapi is installed.

You can find the built ROCgdb executable in ``build/gdb/gdb`` and the *User Manual* in ``build/gdb/doc/gdb.info``.

Install
----------

To install ROCgdb, use:

.. code-block:: bash

  make install

This installs ROCgdb in ``<prefix>/bin/rocgdb``.

Install libraries
-------------------

To execute ROCgdb, you must install the ROCdbgapi library and its dependent ``ROCcomgr`` library. These can be installed as part of the ROCm release using the ``rocm-dbgapi`` package:

- ``librocm-dbgapi.so.0``
- ``libamd_comgr.so.1``

To generate the *User Manual* PDF, use:

.. code-block:: bash

  make pdf

This generates the PDF in ``build/gdb/doc/gdb.pdf``.
