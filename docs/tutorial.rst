.. meta::
  :description: This chapter describes the usage of ROCgdb, a tool for debugging
  ROCm software.
  :keywords: AMD, ROCm, HIP, ROCgdb, performance, debugging

*******************************************************************************
ROCgdb debugger for Linux targets
*******************************************************************************

.. _rocgdb_introduction:
Introduction
===============================================================================
`ROCgdb <https://github.com/ROCm/ROCgdb>`_ is the AMD ROCm debugger for Linux targets.

ROCgdb is an extension to GDB, the GNU Project debugger. The tool provides developers
with a mechanism for debugging ROCm applications running on actual hardware. This tool
enables developers to debug applications without the potential variations introduced
by simulation and emulation environments. It presents a seamless debugging
environment that allows simultaneous GPU and CPU code debugging within the same
application, just like programming in HIP, which is a seamless extension of C++
programming. The existing GDB debugging features are inherently present for debugging
the host code, and additional features have been provided to support debugging ROCm
device code.

ROCgdb supports HIP kernel debugging. It allows you to set breakpoints, single-step
ROCm applications, and inspect and modify the memory and variables of any given thread
running on the hardware.

.. _rocgdb_installation:
Installation
===============================================================================
The ROCm installation also installs the ROCgdb debugger, but some steps are necessary
before using the debugger.

.. _rocgdb_setup:
Setup
===============================================================================
Before debugging, compile your software with debug information. Add the ‘-g’ flag to your
compilation command to do this. This generates debug information even when optimizations
are turned on. Notice that higher optimization levels make the debugging more difficult,
so it might be helpful to turn off these optimizations using the ‘-O0’ compiler option.

.. _rocgdb_debugging:
Debugging
===============================================================================
This section introduces how to use ROCgdb. For more information about GDB, see the `GDB
documentation <https://www.sourceware.org/gdb/documentation/>`_.

First step is to run ROCgdb with your ROCm application:

.. code-block:: shell

    rocgdb my_application

At this point the application is not running, but you'll have access to the debugger
console. Here you can use every gdb option for host debugging and you can use them and
extra ROCgdb specific features for device debugging.

You'll need to set a breakpoint before you run your application with the debugger.

.. code-block:: shell

    tbreak my_app.cpp:458

This will place a breakpoint at the specified line. To start your application use this
command:

.. code-block:: shell

    run

If the breakpoint is in the device code, the debugger will also show the device and host
threads. The device threads will not be individual threads; instead, they represent a
wavefront on the device. You can switch between the device wavefronts as you would
between host threads.

You can also switch between layouts. Use different layouts for different situations while
debugging.

.. code-block:: shell

    layout src
    layout asm

The `src` layout is the source code view, while the `asm` is the assembly view. There are
further layouts you can look up in the `GDB documentation
<https://www.sourceware.org/gdb/documentation/>`_.

.. code-block:: shell

    info threads

This command lists all threads with id and information on where the thread is stopped.

To switch threads you can use the following command:

.. code-block:: shell

    thread <id>

To take a step in the execution use:

.. code-block:: shell

    n

To dump the content of the current wavefronts registers use:

.. code-block:: shell

    i r

The result of this command is just the register dump, which is the all-inclusive data
about the state of the current wavefront, but very difficult to parse.
