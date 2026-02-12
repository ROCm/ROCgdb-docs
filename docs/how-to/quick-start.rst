.. meta::
   :description: Source-level debugger for Linux based on the GNU Debugger
   :keywords: ROCgdb quick start, AMD ROCm Debugger quick start

.. _rocgdb-quick-start:

*********************
ROCgdb quick start
*********************

After :ref:`installing ROCgdb <rocgdb-installation>`, follow the :ref:`setup <rocgdb-setup>` to start debugging your application.

.. _rocgdb-setup:

Setup
=======

Before debugging, compile your software with debug information.

Source compilation
-------------------

To compile your source with debug symbols, use:

.. code-block:: shell

   $ hipcc -ggdb -O0 saxpy.cpp -o saxpy

Adding the ``-g`` flag to your compilation command generates debug information even when optimizations
are turned on. Note that higher optimization levels make debugging more difficult,
so it might be helpful to turn off these optimizations using the ``-O0`` compiler option.

Debugging using ROCgdb
========================

You can either launch and run your application under debugger control or attach debugger to running processes and continue execution.

To start debugging your application under debugger control, follow these steps:

1. Launch your application under debugger control:

   .. code-block:: shell

      $ rocgdb ./saxpy
      […]

   At this point the application is not running, but you'll have access to the debugger
   console. Here you can use every gdb option for host debugging and you can use them and
   extra ROCgdb specific features for device debugging.

2. Set a breakpoint before running the application with debugger.

   .. code-block:: shell

      tbreak my_app.cpp:458

   This places a temporary breakpoint at the specified line. To start your application, use:

   .. code-block:: shell

      (gdb) run

   If the breakpoint is in the device code, the debugger shows the device and host
   threads. The device threads are not individual work items; instead, they represent a
   wavefront on the device. You can switch between the device wavefronts as you can
   between the host threads.

To attach debugger to running processes and continue execution, use:

.. code-block:: shell

   $ rocgdb -pid 1234
   […]
   (gdb) continue

You can also switch between layouts, which allows you to use different layouts for different situations while debugging.

.. code-block:: shell

   layout src
   layout asm

The ``src`` layout is the source code view, while the ``asm`` is the assembly view. For more layouts, see `GDB documentation <https://rocm.docs.amd.com/projects/ROCgdb/en/latest/ROCgdb/gdb/doc/gdb/TUI-Commands.html>`_.

After starting or attaching your application with the debugger, you can utilize these :ref:`rocgdb-essential-commands` to perform further operations.

ROCgdb user guide
===================

The `ROCgdb user guide <https://rocm.docs.amd.com/projects/ROCgdb/en/latest/ROCgdb/gdb/doc/gdb/index.html>`_ provides detailed information about using ROCgdb.
This user guide is also installed in the following directories when you `install ROCm <https://rocm.docs.amd.com/projects/install-on-linux/en/latest/>`_:

- ``/opt/rocm/share/info/rocgdb/gdb.info`` as a texinfo file
- ``/opt/rocm/share/doc/rocgdb/rocgdb.pdf`` as a PDF file

For specific information about debugging heterogeneous programs on ROCm software, refer to the following chapters in the ROCgdb user guide:

- **Debugging Heterogeneous Programs:** Provides general information about
  debugging heterogeneous programs. It also discusses features and commands that are
  not currently implemented but provisionally planned for future versions.

- **Configuration-Specific Information > Architectures > AMD GPU:** Provides
  specific information about debugging heterogeneous programs on ROCm software with
  supported AMD GPU hardware. This section also lists the implementation status
  and known issues of the current version.

You can use the standard `GDB <http://www.gnu.org/software/gdb>`_ commands for both CPU and GPU code debugging.
