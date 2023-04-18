Build the AMD ROCm Debugger
---------------------------

ROCgdb can be built on Ubuntu 18.04, Ubuntu 20.04, Centos 8.1, RHEL 8.1, and SLES
15 Service Pack 1.

Building ROCgdb has the following prerequisites:

1. A C++11 compiler such as GCC 4.8 or Clang 3.3.

2. AMD Debugger API Library (ROCdbgapi) which can be installed as part of the
   AMD ROCm release by the ``rocm-dbgapi`` package.

3. For Ubuntu 18.04 and Ubuntu 20.04 the following adds the needed packages:

   ````shell
   apt install bison flex gcc make ncurses-dev texinfo g++ zlib1g-dev \
     libexpat-dev python3-dev liblzma-dev libgmp-dev libbabeltrace-dev \
     libbabeltrace-ctf-dev
   ````

4. For CentOS 8.1 and RHEL 8.1 the following adds the needed packages:

   ````shell
   yum install -y epel-release centos-release-scl bison flex gcc make \
     texinfo texinfo-tex gcc-c++ zlib-devel expat-devel python3-devel \
     xz-devel gmp-devel libbabeltrace-devel ncurses-devel
   wget http://repo.okay.com.mx/centos/8/x86_64/release/libbabeltrace-devel-1.5.4-2.el8.x86_64.rpm \
   && rpm -ivh --nodeps libbabeltrace-devel-1.5.4-2.el8.x86_64.rpm
   ````

5. For SLES 15 Service Pack 1 the following adds the needed packages:

   ````shell
   zypper in bison flex gcc make texinfo gcc-c++ zlib-devel libexpat-devel \
     python3-devel xz-devel gmp-devel babeltrace-devel ncurses-devel
   ````

An example command-line to build ROCgdb on Linux is:

````shell
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
````

Specify ``--with-rocm-dbgapi=PATH`` if the the AMD Debugger API Library
(ROCdbgapi) is not installed in its default location.  The ``configure`` script
looks in ``PATH/include`` and ``PATH/lib``. The default value for ``PATH`` is
``/opt/rocm``.

The built ROCgdb executable will be placed in:

- ``build/gdb/gdb``

The texinfo *User Manual* will be placed in:

- ``build/gdb/doc/gdb.info``

To install ROCgdb:

````shell
make install
````

The installed ROCgdb will be placed in:

- ``<prefix>/bin/rocgdb``

To execute ROCgdb, the ROCdbgapi library and its dependent ROCcomgr library must
be installed.  These can be installed as part of the AMD ROCm release by the
``rocm-dbgapi`` package:

- ``librocm-dbgapi.so.0``
- ``libamd_comgr.so.1``

The PDF *User Manual* can be generated with:

````shell
make pdf
````

The generated PDF will be placed in:

- ``build/gdb/doc/gdb.pdf``
