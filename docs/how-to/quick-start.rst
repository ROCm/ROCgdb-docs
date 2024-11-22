.. meta::
   :description: Source-level debugger for Linux based on the GNU Debugger
   :keywords: ROCgdb quick start, AMD ROCm Debugger quick start

.. _rocgdb-quick-start:

*******************************************************************************
ROCgdb quick start
*******************************************************************************

After :ref:`installing ROCgdb <rocgdb-installation>`, follow the :ref:`setup <rocgdb-setup>` to start debugging your application.

.. _rocgdb-setup:

Setup
===============================================================================

Before debugging, compile your software with debug information. To achieve this, add the ``-g`` flag to your
compilation command. This generates debug information even when optimizations
are turned on. Note that higher optimization levels make debugging more difficult,
so it might be helpful to turn off these optimizations using the ``-O0`` compiler option.

Debugging using ROCgdb
===============================================================================

To start debugging your application, follow these steps:

1. Run ROCgdb with your ROCm application.

   .. code-block:: shell

    rocgdb my_application

   At this point the application is not running, but you'll have access to the debugger
   console. Here you can use every gdb option for host debugging and you can use them and
   extra ROCgdb specific features for device debugging.

2. Set a breakpoint before running the application with debugger.

   .. code-block:: shell

    tbreak my_app.cpp:458

   This places a breakpoint at the specified line. To start your application, use:

   .. code-block:: shell

    run

   If the breakpoint is in the device code, the debugger shows the device and host
   threads. The device threads are not individual threads; instead, they represent a
   wavefront on the device. You can switch between the device wavefronts as you can
   between the host threads.

3. You can also switch between layouts, which allows you to use different layouts for different situations while debugging.

   .. code-block:: shell

    layout src
    layout asm

   The ``src`` layout is the source code view, while the ``asm`` is the assembly view. For more layouts, see `GDB documentation <https://www.sourceware.org/gdb/documentation/>`_.

   .. code-block:: shell

    info threads

   The preceding command lists all threads with Id and information on where the thread is stopped.

4. To switch threads, use:

   .. code-block:: shell

    thread <id>

5. To take a step in the execution, use:

   .. code-block:: shell

    n

6. To dump the content of the current wavefront's registers, use:

   .. code-block:: shell

    i r

   The result of the preceding command is just the register dump, which is all-inclusive data
   about the state of the current wavefront. This data is very difficult to parse.

ROCgdb user guide
========================

The |ROCgdb user guide| provides detailed information about using ROCgdb.
This user guide is also installed in the following directories when you :doc:`install ROCm <rocm-install-on-linux>`:

- ``/opt/rocm/share/info/rocgdb/gdb.info`` as a texinfo file
- ``/opt/rocm/share/doc/rocgdb/rocgdb.pdf`` as a PDF file

For specific information about debugging heterogeneous programs on ROCm software, refer to the following chapters in the ROCgdb user guide:

- *Debugging Heterogeneous Programs:* It provides general information about
  debugging heterogeneous programs. It also discusses features and commands that are
  not currently implemented but provisionally planned for future versions.
- *Configuration-Specific Information > Architectures > AMD GPU:* It provides
  specific information about debugging heterogeneous programs on ROCm software with
  supported AMDGPU chips. This section also lists the implementation status
  and known issues of the current version.

You can use the standard `GDB <http://www.gnu.org/software/gdb>`_ commands for both CPU and GPU code debugging.

.. |ROCgdb user guide| raw:: html

   <a href="../ROCgdb/gdb/doc/gdb/index.html" target="_blank">ROCgdb debugger manual</a>
