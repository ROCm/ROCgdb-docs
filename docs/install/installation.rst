.. meta::
   :description: Source-level debugger for Linux, based on the GNU Debugger
   :keywords: Install ROCgdb, Build ROCgdb, Install AMD ROCm Debugger, Build AMD ROCm Debugger

.. _rocgdb-installation:

====================
Installing ROCgdb
====================

This topic provides information required to build and install ROCgdb.

System requirements
--------------------

- A system supporting ROCm. See the `supported operating systems <https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-operating-systems>`_.

- A C++17 compiler such as GCC 9 or Clang 5.

- AMD Debugger API Library (``ROCdbgapi``) that can be installed as part of the
  ROCm release using the ``rocm-dbgapi`` package.

- Install the required packages according to the OS:

.. tab-set::

   .. tab-item:: Ubuntu
      :sync: ubuntu

      .. code-block:: shell

        apt install bison flex gcc make ncurses-dev texinfo g++ zlib1g-dev \
        libexpat-dev python3-dev liblzma-dev libgmp-dev libmpfr-dev

   .. tab-item:: RHEL
      :sync: rhel

      .. code-block:: shell

        yum install -y epel-release centos-release-scl bison flex gcc make \
        texinfo texinfo-tex gcc-c++ zlib-devel expat-devel python3-devel \
        xz-devel gmp-devel ncurses-devel mpfr-devel

   .. tab-item:: SLES
      :sync: sles

      .. code-block:: shell

        zypper in bison flex gcc make texinfo gcc-c++ zlib-devel libexpat-devel \
        python3-devel xz-devel gmp-devel ncurses-devel mpfr-devel

.. note::

  ROCgdb might become unresponsive in SELinux-enabled distributions. To learn more about this issue, see `installation troubleshooting <https://rocm.docs.amd.com/projects/install-on-linux-internal/en/latest/reference/install-faq.html#issue-10-rocm-debugging-tools-might-become-unresponsive-in-selinux-enabled-distributions>`_.

Building ROCgdb
----------------

An example command line to build ROCgdb on Linux:

.. code-block:: bash

  cd rocgdb
  mkdir build
  cd build
  ../configure --program-prefix=roc \
  --enable-64-bit-bfd --enable-targets="x86_64-linux-gnu,amdgcn-amd-amdhsa" \
  --disable-ld --disable-gas --disable-gdbserver --disable-sim --enable-tui \
  --disable-gdbtk --disable-gprofng --disable-shared --with-expat \
  --with-system-zlib --without-guile --without-babeltrace --with-lzma \
  --with-python=python3
  make

If ``ROCdbgapi`` is not installed in the system's default location, specify ``PKG_CONFIG_PATH`` to make the correct build configuration available to ``pkg-config``.
If ``ROCdbgapi`` is installed in ``/opt/rocm-$ROCM_VERSION`` (default for ROCm packages), use ``PKG_CONFIG_PATH=/opt/rocm-$ROCM_VERSION/share/pkgconfig``.

If the system's dynamic linker is not configured to locate ``ROCdbgapi`` where it is
installed, configure and build ROCgdb using ``LDFLAGS="-Wl,-rpath=/opt/rocm-$ROCM_VERSION/lib"``.
Alternatively, use ``LD_LIBRARY_PATH`` at runtime to indicate where ``ROCdbgapi`` is installed.

You can find the built ROCgdb executable in ``build/gdb/gdb`` and the user manual in ``build/gdb/doc/gdb.info``.

Installing ROCgdb
------------------

To install ROCgdb, use:

.. code-block:: bash

  make install

This installs ROCgdb in ``<prefix>/bin/rocgdb``.

Installing libraries
---------------------

To execute ROCgdb, you must install the ``ROCdbgapi`` library and its dependent ``Comgr`` library. These can be installed as part of the ROCm release using the ``rocm-dbgapi`` package:

- ``librocm-dbgapi.so.0``
- ``libamd_comgr.so``

To generate the ROCgdb user guide as a PDF, use:

.. code-block:: bash

  make pdf

This generates the PDF in ``build/gdb/doc/gdb.pdf``.

.. note::

  For ROCgdb user guide in HTML format, see `ROCgdb user guide <https://rocm.docs.amd.com/projects/ROCgdb/en/latest/ROCgdb/gdb/doc/gdb/index.html>`_.
