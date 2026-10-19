.. meta::
   :description: Find the ROCgdb command for a task, such as inspecting GPU state, printing and changing data, switching waves and lanes, and controlling execution.
   :keywords: ROCgdb commands, AMD ROCm Debugger quick start, ROCgdb quick reference

.. _rocgdb-essential-commands:

****************
Commands by task
****************

Find the ROCgdb command for what you want to do. Sample output is collapsed under each table, and it differs on your system.

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - I want to
     - Go to
   * - Look at code, agents, queues, waves, lanes, frames, and registers
     - `Inspect kernel state`_
   * - Print a variable, array, or expression
     - `Print kernel data`_
   * - Change a variable
     - `Modify kernel data`_
   * - Switch to another thread, lane, or frame
     - `Change kernel focus`_
   * - Set breakpoints, step, and resume
     - `Control kernel execution`_

Inspect kernel state
====================

Source and disassembly
----------------------

.. list-table::
   :header-rows: 1
   :widths: 35 30 35

   * - Task
     - Command
     - Notes
   * - View kernel code
     - ``list``
     -
   * - View disassembly
     - ``disassemble``
     -

.. dropdown:: Sample output: ``list``

   .. code-block:: text

       1  #include <hip/hip_runtime.h>
       2  #include <algorithm>
       3  #include <iostream>
       4  #include <numeric>
       5  #include <vector>
       6  #include <cstddef>
       8  __global__ void saxpy_kernel(const float a, const float* d_x, float* d_y, const unsigned int size)
       9  {
       10      // Compute the current thread's index in the grid.
       11      const unsigned int global_idx = blockIdx.x * blockDim.x + threadIdx.x;
       12      // The grid can be larger than the number of items in the vectors. Avoid out-of-bounds addressing.
       13      if(global_idx < size)
       14      {
       15          d_y[global_idx] = a * d_x[global_idx] + d_y[global_idx];
       16      }
       17  }
       18  int main()
       19  {
       ....
       99  }

.. dropdown:: Sample output: ``disassemble``

   .. code-block:: shell

       Dump of assembler code for function _ZL3bari:
           0x00007ffff608e2b0 <+0>:     s_waitcnt vmcnt(0) expcnt(0) lgkmcnt(0)
           0x00007ffff608e2b4 <+4>:     s_mov_b32 s25, s33
           0x00007ffff608e2b8 <+8>:     s_mov_b32 s33, s32
           0x00007ffff608e2bc <+12>:    s_xor_saveexec_b64 s[16:17], -1
           0x00007ffff608e2c0 <+16>:    buffer_store_dword v36, off, s[0:3], s33 offset:52
           .....
           0x00007ffff608e92c <+1660>:  s_mov_b64 exec, s[4:5]
           0x00007ffff608e930 <+1664>:  s_mov_b32 s33, s25
           0x00007ffff608e934 <+1668>:  s_waitcnt vmcnt(0)
           0x00007ffff608e938 <+1672>:  s_setpc_b64 s[30:31]
       End of assembler dump.

Heterogeneous system state
--------------------------

These commands show the agents, queues, dispatches, threads, and lanes of a heterogeneous program.

.. list-table::
   :header-rows: 1
   :widths: 20 25 55

   * - Task
     - Command
     - Notes
   * - List agents
     - ``info agents``
     - Lists each heterogeneous agent. See `info agents command <https://rocm.docs.amd.com/projects/ROCgdb/en/latest/ROCgdb/gdb/doc/gdb/Heterogeneous-Debugging.html#index-info-agents>`_.
   * - List queues
     - ``info queues``
     - Lists each heterogeneous queue. See `info queues command <https://rocm.docs.amd.com/projects/ROCgdb/en/latest/ROCgdb/gdb/doc/gdb/Heterogeneous-Debugging.html#index-info-queues>`_.
   * - List dispatches
     - ``info dispatches``
     - Lists each heterogeneous dispatch. See `info dispatches command <https://rocm.docs.amd.com/projects/ROCgdb/en/latest/ROCgdb/gdb/doc/gdb/Heterogeneous-Debugging.html#index-info-dispatches>`_.
   * - List CPU threads and GPU waves
     - ``info threads``
     - Lists the threads created on all heterogeneous agents. See `Debugging programs with multiple threads <https://rocm.docs.amd.com/projects/ROCgdb/en/latest/ROCgdb/gdb/doc/gdb/Threads.html>`_.
   * - List the lanes of the current wave
     - ``info lanes``
     - Displays information about individual source language threads of execution that are mapped to SIMD-like lanes of a thread. On target architectures that support Single Instruction Multiple Data (SIMD) or Single Instruction Multiple Threads (SIMT) instructions, a single machine instruction can operate in parallel on multiple lanes. See `Debugging heterogeneous programs <https://rocm.docs.amd.com/projects/ROCgdb/en/latest/ROCgdb/gdb/doc/gdb/Heterogeneous-Debugging.html>`_.

.. dropdown:: Sample output: ``info agents``

   .. code-block:: shell

         Id State Target Id                  Architecture Device Name        Cores Threads Location
       * 1  A     AMDGPU Agent (GPUID 35090) gfx90a       AMD Instinct MI210 416   3328    0000:4a:00.0
         2  A     AMDGPU Agent (GPUID 34915) gfx90a       AMD Instinct MI210 416   3328    0000:09:00.0
         3  A     AMDGPU Agent (GPUID 56224) gfx90a       AMD Instinct MI210 416   3328    0000:0c:00.0
         4  A     AMDGPU Agent (GPUID 33385) gfx90a       AMD Instinct MI210 416   3328    0000:11:00.0

.. dropdown:: Sample output: ``info queues``

   .. code-block:: shell

         Id   Target Id                Type         Read   Write  Size     Address
         1    AMDGPU Queue 1:1 (QID 0) HSA          2      2      4096     0x00007ffff626e000
       * 2    AMDGPU Queue 1:2 (QID 1) HSA          0      2      1048576  0x00007fffe5800000

.. dropdown:: Sample output: ``info dispatches``

   .. code-block:: shell

          Id   Target Id                      Grid    Workgroup Fence   Kernel Function
        * 1    AMDGPU Dispatch 1:2:1 (PKID 0) [1,1,1] [1,1,1]   B|Aa|Ra kern()

.. dropdown:: Sample output: ``info threads``

   .. code-block:: shell

         Id   Target Id                                    Frame
         1    Thread 0x7ffff648bf80 (LWP 1981864) "saxpy" 0x00007ffff5a6c9ef in ?? () from /opt/rocm-7.1.0/lib/libhsa-runtime64.so.1
         2    Thread 0x7ffff55ff6c0 (LWP 1981871) "saxpy" __GI___ioctl (fd=3, request=3222817548) at ../sysdeps/unix/sysv/linux/ioctl.c:36
         4    Thread 0x7fffeffff6c0 (LWP 1981873) "saxpy" __GI___ioctl (fd=3, request=3222817548) at ../sysdeps/unix/sysv/linux/ioctl.c:36
         6    Thread 0x7ffff5dff6c0 (LWP 1981877) "saxpy" __GI___ioctl (fd=3, request=3222817548) at ../sysdeps/unix/sysv/linux/ioctl.c:36
       * 7    AMDGPU Wave 1:2:1:1 (0,0,0)/0 "saxpy"       saxpy_kernel () at saxpy.cpp:8

.. dropdown:: Sample output: ``info lanes``

   .. code-block:: shell

         Id   State Target Id                            Frame
       * 0    A     AMDGPU Lane 1:2:1:1/0 (0,0,0)[0,0,0] kern () at /home/user/saxpy.cpp:7

Frames and variables
--------------------

.. list-table::
   :header-rows: 1
   :widths: 35 30 35

   * - Task
     - Command
     - Notes
   * - View the back trace
     - ``backtrace``
     -
   * - View the current stack frame
     - ``info frame``
     -
   * - View frame arguments
     - ``info args``
     -
   * - View frame local variables
     - ``info locals``
     -

.. dropdown:: Sample output: ``backtrace``

   .. code-block:: shell

       #0  saxpy (tid=0) at /home/user/saxpy.cpp:33
       #1  0x00007ffff608ee40 in kern () at /home/user/saxpy.cpp:4

.. dropdown:: Sample output: ``info frame``

   .. code-block:: shell

       Stack level 0, frame at private_wave#0x800:
       pc = 0x7ffff608e3bc in bar (/home/user/saxpy.cpp:33); saved pc = 0x7ffff608ee40
       called by frame at private_wave#0x0
       source language c++.
       Arglist at private_wave#0x800, args: tid=0
       Locals at private_wave#0x800, Saved registers:
       v36 at private_wave#0x1500, v37 at private_wave#0x1600

.. dropdown:: Sample output: ``info args``

   .. code-block:: shell

       tid = 0

.. dropdown:: Sample output: ``info locals``

   .. code-block:: shell

       No locals.

Registers and memory
--------------------

.. list-table::
   :header-rows: 1
   :widths: 35 30 35

   * - Task
     - Command
     - Notes
   * - View GPU registers
     - ``info registers``
     - Dumps the general-purpose registers, which provide all-inclusive data about the state of the current wavefront.
   * - View all GPU registers
     - ``info all-registers``
     - Dumps all registers, not only the general-purpose registers.

.. dropdown:: Sample output: ``info registers``

   .. code-block:: shell

       v0             {0x30 <repeats 64 times>}
       ....
       s41            0x0                 0
       m0             0x1008              4104
       pc             0x7ffff608e3bc      0x7ffff608e3bc <saxpy(int)+268>
       exec           0x5555555555555555  6148914691236517205
       vcc            0xffffffffffffffff  18446744073709551615

To view GPU data in an address space, use the ``x`` command with the address space and address:

.. code-block:: shell

    (gdb) x/nfu global#0xdeadbeef
    (gdb) x/nfu local#0xdeadbeef
    (gdb) x/nfu generic#0xdeadbeef
    (gdb) x/nfu private_wave#0xdeadbeef
    (gdb) x/nfu private_lane#0xdeadbeef

For more information, see `AMD GPU address spaces <https://rocm.docs.amd.com/projects/ROCgdb/en/latest/ROCgdb/gdb/doc/gdb/AMD-GPU.html#AMD-GPU-Address-Spaces>`_.

Print kernel data
=================

.. list-table::
   :header-rows: 1
   :widths: 25 40 35

   * - Task
     - Command
     - Example
   * - Print a variable
     - ``print <variable>``
     - ``print foo``
   * - Print an array
     - ``print *<address>@<count>``
     - ``print *foo[2]@8``
   * - Print an expression
     - ``print <expression>``
     - ``print foo[4] >> 1``
   * - Print in a format
     - ``p/<code> <value>``
     - ``p/x foo[1]``

The values for ``<code>`` are:

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Code
     - Format
   * - ``x``
     - Hexadecimal
   * - ``d``
     - Decimal
   * - ``u``
     - Unsigned decimal
   * - ``o``
     - Octal
   * - ``t``
     - Binary (two)
   * - ``a``
     - Address (hex + offset)
   * - ``c``
     - Character
   * - ``f``
     - Float
   * - ``s``
     - String
   * - ``z``
     - Hexadecimal with leading zeros
   * - ``r``
     - Raw (skips pretty printing)

Modify kernel data
==================

.. list-table::
   :header-rows: 1
   :widths: 35 35 30

   * - Task
     - Command
     - Example
   * - Modify kernel data directly
     - ``set var <variable>=<value>``
     - ``set var foo[1]=45``
   * - Modify kernel data indirectly
     - ``print <variable>=<value>``
     - ``print foo[3]=3``

Change kernel focus
===================

.. list-table::
   :header-rows: 1
   :widths: 35 30 35

   * - Task
     - Command
     - Example
   * - Change thread
     - ``thread <id>``
     - ``thread 9``
   * - Change lane
     - ``lane <id>``
     - ``lane 5``
   * - Select a frame
     - ``frame <index>``
     -
   * - Move up the stack
     - ``up <count>``
     -
   * - Move down the stack
     - ``down <count>``
     -

Control kernel execution
========================

Set breakpoints
---------------

.. code-block:: shell

    (gdb) break saxpy.cpp:47
    (gdb) break func_foo
    (gdb) break *0x01234567

To set a temporary breakpoint, use ``tbreak``:

.. code-block:: shell

    (gdb) tbreak saxpy.cpp:47
    (gdb) tbreak func_foo
    (gdb) tbreak +24

Set conditional breakpoints
---------------------------

.. code-block:: shell

    (gdb) break func_foo if idx == 9
    (gdb) break func_foo if $_agent == 2
    (gdb) break func_foo if $_queue == 1
    (gdb) break func_foo if $_dispatch == 6
    (gdb) break func_foo if $_thread == 7
    (gdb) break func_foo if $_lane == 15
    (gdb) break func_foo if $_thread_workgroup_pos == 3
    (gdb) break func_foo if $_lane_workgroup_pos == "[0,0,0]"

Set watchpoints and catchpoints
-------------------------------

.. code-block:: shell

    (gdb) watch foo[4]

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Command
     - Catches
   * - ``catch load``
     - Loads of shared libraries (debug dynamic linking).
   * - ``catch unload``
     - Unloads of shared libraries (track cleanup and unloading).
   * - ``catch rethrow``
     - An exception when it is rethrown (trace exception propagation).
   * - ``catch signal SIGSEGV``
     - Signals by name or number (debug crashes or signals).
   * - ``catch syscall open``
     - System calls by name, group, or number (trace system-level calls).
   * - ``catch throw``
     - An exception when it is thrown (trace exception origins).
   * - ``catch vfork``
     - Calls to ``vfork`` (monitor child process creation).

Set scheduler modes
-------------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Task
     - Command
     - More information
   * - Lock the scheduler (waves)
     - ``set scheduler-locking on``
     - `Scheduler locking mode <https://rocm.docs.amd.com/projects/ROCgdb/en/latest/ROCgdb/gdb/doc/gdb/All_002dStop-Mode.html#set-scheduler_002dlocking>`_
   * - Turn on non-stop mode
     - ``set non-stop on``
     - `Non-stop mode <https://rocm.docs.amd.com/projects/ROCgdb/en/latest/ROCgdb/gdb/doc/gdb/Non_002dStop-Mode.html>`_
   * - Turn on all-stop mode
     - ``set non-stop off``
     - `All-stop mode <https://rocm.docs.amd.com/projects/ROCgdb/en/latest/ROCgdb/gdb/doc/gdb/All_002dStop-Mode.html>`_

Manage breakpoints, watchpoints, and catchpoints
------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 30 35

   * - Task
     - Command
     - Example
   * - Disable
     - ``disable <list>``
     - ``disable 4``
   * - Enable
     - ``enable <list>``
     - ``enable 4``
   * - Delete
     - ``delete <list>``
     - ``delete 4``

Step and resume
---------------

.. list-table::
   :header-rows: 1
   :widths: 35 30 35

   * - Task
     - Command
     - Example
   * - Step one source line
     - ``step``, ``next``
     -
   * - Step several source lines
     - ``step <count>``, ``next <count>``
     - ``step 3``, ``next 3``
   * - Continue until a later source line
     - ``until``
     -
   * - Continue until an address
     - ``until <address>``
     - ``until 0x0000ffffdeadbeef``
   * - Run until the current frame returns
     - ``finish``
     -
   * - Step one machine instruction
     - ``stepi``, ``nexti``
     -
   * - Resume execution
     - ``continue``
     -

To run commands automatically when a breakpoint is hit, use a command sequence:

.. code-block:: shell

    (gdb) break saxpy.cpp:47
    command BREAKPOINT_NUMBER
    continue
    end

Can't find a command?
=====================

* For the AMD GPU commands and the debugging model, see `Debugging on AMD GPU <../ROCgdb/gdb/doc/gdb/AMD-GPU.html>`_ in the ROCgdb user guide.
* For every GDB command, see the `full user guide <../ROCgdb/gdb/doc/gdb/index.html>`_.
* If a command or sample on this page is wrong or missing, `open an issue <https://github.com/ROCm/ROCgdb/issues>`_.
