.. meta::
   :description: Find the ROCgdb command for a task, such as inspecting GPU state, printing and changing kernel data, switching waves and lanes, and controlling execution.
   :keywords: ROCgdb commands, AMD ROCm Debugger quick start, ROCgdb quick reference

.. _rocgdb-essential-commands:

****************
Commands by task
****************

Find the ROCgdb command for what you want to do. For the inspection commands, a sample of the output follows each table.

This page uses the terms :term:`agent <HSA agent>`, :term:`wave`, and :term:`lane`. :ref:`rocgdb-gpu-execution-state` defines them.

.. note::

   The sample output is illustrative. The samples come from different sessions and programs, so thread IDs, addresses, file names, line numbers, and kernel names vary from sample to sample. Your output differs too.

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - I want to
     - Go to
   * - Attach to a program that is already running
     - `Attach to a running process`_
   * - Look at code, agents, queues, dispatches, waves, lanes, frames, registers, and memory
     - `Inspect kernel state`_
   * - Print a variable, array, or expression
     - `Print kernel data`_
   * - Change a variable
     - `Modify kernel data`_
   * - Switch to another thread, lane, or frame
     - `Change kernel focus`_
   * - Set breakpoints, step, and resume
     - `Control kernel execution`_

.. _rocgdb-commands-attach:

Attach to a running process
===========================

To attach ROCgdb to a program that's already running, find its process ID with ``pgrep -a <program-name>``, then attach:

.. code-block:: shell

   $ rocgdb -p <process-id>
   […]
   (gdb) continue

For the full procedure, including what to do if the attach fails, see :ref:`rocgdb-attach`.

Inspect kernel state
====================

Use these commands to look at code, agents, queues, dispatches, waves, lanes, frames, registers, and memory.

Source and disassembly
----------------------

Use these commands to view source lines and machine instructions.

.. list-table::
   :header-rows: 1
   :widths: 35 30 35

   * - Task
     - Command
     - Notes
   * - View kernel code
     - ``list``
     - Shows the source lines around the current line. Run ``list`` again to see the next lines.
   * - View disassembly
     - ``disassemble``
     - Shows the machine instructions of the current function.
   * - Show the source view
     - ``layout src``
     - Opens the text user interface (TUI) with the source code. For more layouts, see `TUI-specific commands <../ROCgdb/gdb/doc/gdb/TUI-Commands.html>`_.
   * - Show the assembly view
     - ``layout asm``
     - Opens the TUI with the assembly code.

Sample output for ``list``, stopped in the kernel:

.. code-block:: text

   (gdb) list
   34      /// \brief Calculates \p d_y[i]=a*d_x[i]+d_y[i] where \p i stands for the
   35      /// thread's index in the grid.
   36      __global__ void saxpy_kernel(const float a, const float *d_x, float *d_y,
   37                                   const unsigned int size) {
   38        // Compute the current thread's index in the grid.
   39        const unsigned int global_idx = blockIdx.x * blockDim.x + threadIdx.x;
   40
   41        // The grid can be larger than the number of items in the vectors. Avoid
   42        // out-of-bounds addressing.
   43        if (global_idx < size) {
   (gdb) list
   44          d_y[global_idx] = a * d_x[global_idx] + d_y[global_idx];
   45        }
   ...

Sample output for ``disassemble``:

.. code-block:: text

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

These commands show the agents, queues, dispatches, threads, waves, and lanes of your program.

.. list-table::
   :header-rows: 1
   :widths: 20 25 55

   * - Task
     - Command
     - Notes
   * - List agents
     - ``info agents``
     - Shows each agent, such as an AMD GPU, in the system. See `info agents command <../ROCgdb/gdb/doc/gdb/Heterogeneous-Debugging.html#index-info-agents>`_.
   * - List queues
     - ``info queues``
     - Shows each queue that receives kernel dispatches. See `info queues command <../ROCgdb/gdb/doc/gdb/Heterogeneous-Debugging.html#index-info-queues>`_.
   * - List dispatches
     - ``info dispatches``
     - Shows each kernel launch. See `info dispatches command <../ROCgdb/gdb/doc/gdb/Heterogeneous-Debugging.html#index-info-dispatches>`_.
   * - List CPU threads and GPU waves
     - ``info threads``
     - Shows the CPU threads and the GPU waves. Every wave is a thread, so a GPU program can list thousands. Limit the output with a range, such as ``info threads 1-10``. See `Debugging programs with multiple threads <../ROCgdb/gdb/doc/gdb/Threads.html>`_.
   * - List the lanes of the current wave
     - ``info lanes``
     - Shows the lanes of the current wave and whether each one is active (``A``) or inactive (``I``). Use it to find the lane to inspect. See `Debugging heterogeneous programs <../ROCgdb/gdb/doc/gdb/Heterogeneous-Debugging.html>`_.

Sample output for ``info agents``:

.. code-block:: text

      Id State Target Id                  Architecture Device Name        Cores Threads Location
    * 1  A     AMDGPU Agent (GPUID 35090) gfx90a       AMD Instinct MI210 416   3328    0000:4a:00.0
      2  A     AMDGPU Agent (GPUID 34915) gfx90a       AMD Instinct MI210 416   3328    0000:09:00.0
      3  A     AMDGPU Agent (GPUID 56224) gfx90a       AMD Instinct MI210 416   3328    0000:0c:00.0
      4  A     AMDGPU Agent (GPUID 33385) gfx90a       AMD Instinct MI210 416   3328    0000:11:00.0

Sample output for ``info queues``:

.. code-block:: text

      Id   Target Id                Type         Read   Write  Size     Address
      1    AMDGPU Queue 1:1 (QID 0) HSA          2      2      4096     0x00007ffff626e000
    * 2    AMDGPU Queue 1:2 (QID 1) HSA          0      2      1048576  0x00007fffe5800000

This sample shows only part of the output. The number of queues depends on the application and the runtime.

Sample output for ``info dispatches``:

.. code-block:: text

      Id   Target Id                      Grid          Cluster Workgroup Fence   Kernel Function
    * 1    AMDGPU Dispatch 1:1:1 (PKID 1) [1000192,1,1] -       [256,1,1] B|As|Rs saxpy_kernel(float, float const*, float*, unsigned int)

``info dispatches`` lists the dispatch reliably only while you're stopped inside the kernel. At the host line that launches the kernel, it prints ``No dispatches are currently active.`` because the launch hasn't happened yet.

The **Cluster** column is the launch's cluster dimensions. It shows ``-`` when the kernel doesn't use workgroup clusters.

The ``Fence`` column shows the memory fences that the dispatch packet requests, separated by ``|``:

* ``B``: The barrier bit is set. The next packet in the queue doesn't start until this dispatch completes.
* ``Aa`` or ``As``: An acquire fence at agent scope (``a``) or system scope (``s``) runs before the dispatch.
* ``Ra`` or ``Rs``: A release fence at agent scope (``a``) or system scope (``s``) runs when the dispatch completes.

In the sample, ``B|As|Rs`` means a barrier with acquire and release fences at system scope.

Sample output for ``info threads``. The full listing is long, because every wave is a thread, so limit the range:

.. code-block:: text

   (gdb) info threads 1-10
     Id   Target Id                                    Frame
     1    Thread 0x7ffff6fe5500 (LWP 3349951) "saxpy"  0x00007fffec6ea7d3 in rocr::core::BusyWaitSignal::WaitRelaxed(hsa_signal_condition_t, long, unsigned long, hsa_wait_state_t) ()
      from /opt/rocm/lib/libhsa-runtime64.so.1
     2    Thread 0x7fffeb3ff6c0 (LWP 3349954) "saxpy"  __GI___ioctl (fd=3, request=3222817548) at ../sysdeps/unix/sysv/linux/ioctl.c:36
     3    Thread 0x7fffe29ff6c0 (LWP 3349955) "saxpy"  __GI___ioctl (fd=3, request=3222817548) at ../sysdeps/unix/sysv/linux/ioctl.c:36
     5    Thread 0x7fffe21fe6c0 (LWP 3349958) "saxpy"  __GI___ioctl (fd=3, request=3222817548) at ../sysdeps/unix/sysv/linux/ioctl.c:36
   * 6    AMDGPU Wave 1:1:1:1 (0,0,0)/0 "saxpy_kernel" saxpy_kernel (a=2, d_x=0x7fffe9c00000, d_y=0x7fffe9600000, size=1000000) at main.hip:39
     7    AMDGPU Wave 1:1:1:2 (0,0,0)/1 "saxpy_kernel" __hip_get_block_dim_x () at /opt/rocm/include/hip/amd_detail/amd_hip_runtime.h:255
     8    AMDGPU Wave 1:1:1:3 (0,0,0)/2 "saxpy_kernel" __hip_get_block_dim_x () at /opt/rocm/include/hip/amd_detail/amd_hip_runtime.h:255
     9    AMDGPU Wave 1:1:1:4 (0,0,0)/3 "saxpy_kernel" __hip_get_block_dim_x () at /opt/rocm/include/hip/amd_detail/amd_hip_runtime.h:255
     10   AMDGPU Wave 1:1:1:5 (8,0,0)/0 "saxpy_kernel" __hip_get_block_dim_x () at /opt/rocm/include/hip/amd_detail/amd_hip_runtime.h:255

The CPU threads keep the program name, ``"saxpy"``. The wave rows use the kernel name, ``"saxpy_kernel"``, in quotes.

Sample output for ``info lanes``:

.. code-block:: text

   (gdb) info lanes
     Id   State Target Id                              Frame
   * 0    A     AMDGPU Lane 1:1:1:1/0 (0,0,0)[0,0,0]   saxpy_kernel (a=2, d_x=0x7fffe9c00000, d_y=0x7fffe9600000, size=1000000) at main.hip:39
     1    A     AMDGPU Lane 1:1:1:1/1 (0,0,0)[1,0,0]   saxpy_kernel (a=2, d_x=0x7fffe9c00000, d_y=0x7fffe9600000, size=1000000) at main.hip:39
     2    A     AMDGPU Lane 1:1:1:1/2 (0,0,0)[2,0,0]   saxpy_kernel (a=2, d_x=0x7fffe9c00000, d_y=0x7fffe9600000, size=1000000) at main.hip:39
     ...

``info lanes`` prints one row for every lane in the wave, 64 on gfx9 GPUs such as gfx90a, gfx942, and gfx950, and 32 on wave32 GPUs such as gfx1100 and gfx1201. This sample shows only the first three lanes.

Frames and variables
--------------------

Use these commands to view the call stack and the arguments and local variables of a frame.

.. list-table::
   :header-rows: 1
   :widths: 35 30 35

   * - Task
     - Command
     - Notes
   * - View the call stack
     - ``backtrace``
     - Shows the call stack of the current wave or thread.
   * - View the current stack frame
     - ``info frame``
     - Shows the address, saved registers, and source language of the current frame.
   * - View frame arguments
     - ``info args``
     - Shows the arguments of the current frame.
   * - View frame local variables
     - ``info locals``
     - Shows the local variables of the current frame.

Sample output for ``backtrace``:

.. code-block:: text

    #0  bar (tid=0) at /home/user/saxpy.cpp:33
    #1  0x00007ffff608ee40 in kern () at /home/user/saxpy.cpp:4

Sample output for ``info frame``:

.. code-block:: text

    Stack level 0, frame at private_wave#0x800:
    pc = 0x7ffff608e3bc in bar (/home/user/saxpy.cpp:33); saved pc = 0x7ffff608ee40
    called by frame at private_wave#0x0
    source language c++.
    Arglist at private_wave#0x800, args: tid=0
    Locals at private_wave#0x800, Saved registers:
    v36 at private_wave#0x1500, v37 at private_wave#0x1600

Sample output for ``info args``:

.. code-block:: text

    tid = 0

Sample output for ``info locals``:

.. code-block:: text

    No locals.

Registers and memory
--------------------

Use these commands to view the registers of the current wave and the contents of GPU memory.

.. list-table::
   :header-rows: 1
   :widths: 35 30 35

   * - Task
     - Command
     - Notes
   * - View GPU registers
     - ``info registers``
     - Shows the general-purpose registers of the current wave.
   * - View all GPU registers
     - ``info all-registers``
     - Shows all registers, not only the general-purpose registers.
   * - View GPU memory
     - ``x/<format> <space>#<address>``
     - Prints memory in an AMD GPU address space. See the examples after the sample output.

Sample output for ``info registers``:

.. code-block:: text

    v0             {0x30 <repeats 64 times>}
    ....
    s41            0x0                 0
    m0             0x1008              4104
    pc             0x7ffff608e3bc      0x7ffff608e3bc <bar(int)+268>
    exec           0x5555555555555555  6148914691236517205
    vcc            0xffffffffffffffff  18446744073709551615

Without a format, ``x`` prints one word in hexadecimal. Without ``<space>#``, ROCgdb uses the default address space, ``global``. In the following examples, the ``/4xw`` format prints four (``4``) words (``w``) in hexadecimal (``x``), and ``0x0000ffffdeadbeef`` is a placeholder address:

.. code-block:: shell

    (gdb) x/4xw global#0x0000ffffdeadbeef
    (gdb) x/4xw local#0x0000ffffdeadbeef
    (gdb) x/4xw generic#0x0000ffffdeadbeef
    (gdb) x/4xw private_wave#0x0000ffffdeadbeef
    (gdb) x/4xw private_lane#0x0000ffffdeadbeef

For more information, see `AMD GPU address spaces <../ROCgdb/gdb/doc/gdb/AMD-GPU.html#AMD-GPU-Address-Spaces>`_.

.. _rocgdb-commands-print:

Print kernel data
=================

Use ``print`` to show the value of a variable, an array slice, or an expression in the current lane.

.. list-table::
   :header-rows: 1
   :widths: 25 40 35

   * - Task
     - Command
     - Example
   * - Print a variable
     - ``print <variable>``
     - ``print foo``
   * - Print part of an array
     - ``print <array>[<index>]@<count>``
     - ``print foo[2]@8``
   * - Print memory through a pointer
     - ``print *<pointer>@<count>``
     - ``print *ptr@8``
   * - Print an expression
     - ``print <expression>``
     - ``print foo[4] >> 1``
   * - Print in a format
     - ``print/<code> <value>``
     - ``print/x foo[1]``

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
     - Binary
   * - ``a``
     - Address, in hexadecimal and as an offset from the nearest symbol
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

Use ``set var`` or ``print`` to change a value. ROCgdb evaluates the expression in the current lane. A change to global memory is visible to every lane. ``print`` also shows the new value.

.. list-table::
   :header-rows: 1
   :widths: 35 35 30

   * - Task
     - Command
     - Example
   * - Change a variable
     - ``set var <variable>=<value>``
     - ``set var foo[1]=45``
   * - Change a variable and print the new value
     - ``print <variable>=<value>``
     - ``print foo[3]=3``

Change kernel focus
===================

Use these commands to choose the thread, wave, lane, or frame that other commands apply to.

.. list-table::
   :header-rows: 1
   :widths: 35 30 35

   * - Task
     - Command
     - Notes
   * - Select a thread or wave
     - ``thread <id>``
     - Selects a CPU thread or GPU wave by its ``Id`` in the ``info threads`` output. For example, ``thread 9``.
   * - Select a lane
     - ``lane <id>``
     - Selects a lane of the current wave by its ``Id`` in the ``info lanes`` output. For example, ``lane 5``.
   * - Select a frame
     - ``frame <index>``
     - Selects a frame by its number in the ``backtrace`` output. Frame 0 is the innermost frame. For example, ``frame 1`` selects the caller of the function in frame 0.
   * - Move up the stack
     - ``up <count>``
     - Moves ``<count>`` frames toward the caller. For example, ``up 2`` selects the caller of the caller.
   * - Move down the stack
     - ``down <count>``
     - Moves ``<count>`` frames back toward frame 0. For example, ``down 1`` selects the frame that the current frame called.

Control kernel execution
========================

Use these commands to stop the program where you want, step through it, and resume it.

Set breakpoints
---------------

To stop at a function, a source line, or an address, use ``break``:

.. code-block:: shell

    (gdb) break <file>:<line-number>
    (gdb) break func_foo
    (gdb) break *0x0000ffffdeadbeef

To set a temporary breakpoint, use ``tbreak``:

.. code-block:: shell

    (gdb) tbreak <file>:<line-number>
    (gdb) tbreak func_foo
    (gdb) tbreak +24

Set conditional breakpoints
---------------------------

To stop only when a condition is true, add ``if <condition>`` to ``break``. The condition can use a program variable or a ROCgdb convenience variable for the current agent, queue, dispatch, thread, or lane:

.. code-block:: shell

    (gdb) break func_foo if idx == 9
    (gdb) break func_foo if $_agent == 2
    (gdb) break func_foo if $_queue == 1
    (gdb) break func_foo if $_dispatch == 6
    (gdb) break func_foo if $_thread == 7
    (gdb) break func_foo if $_lane == 15
    (gdb) break func_foo if $_streq($_thread_workgroup_pos, "3")
    (gdb) break func_foo if $_streq($_lane_workgroup_pos, "[0,0,0]")

Set watchpoints and catchpoints
-------------------------------

To stop when a value changes, use ``watch``:

.. code-block:: shell

    (gdb) watch foo[4]

To stop when an event happens, use ``catch``:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Command
     - Catches
   * - ``catch hiperr``
     - A failed HIP API call (find HIP errors before you debug a kernel). Requires ROCm 7.14 or later.
   * - ``catch load``
     - Loads of shared libraries (debug dynamic linking).
   * - ``catch rethrow``
     - An exception when it is rethrown (trace exception propagation).
   * - ``catch signal SIGSEGV``
     - Signals by name or number (debug crashes or signals).
   * - ``catch syscall openat``
     - System calls by name, group, or number (trace system-level calls).
   * - ``catch throw``
     - An exception when it is thrown (trace exception origins).
   * - ``catch unload``
     - Unloads of shared libraries (track cleanup and unloading).
   * - ``catch vfork``
     - Calls to ``vfork`` (monitor child process creation).

Set scheduler modes
-------------------

Use these commands to choose which threads and waves resume when you step or continue.

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Task
     - Command
     - More information
   * - Resume only the current thread or wave
     - ``set scheduler-locking on``
     - `Scheduler locking mode <../ROCgdb/gdb/doc/gdb/All_002dStop-Mode.html#set-scheduler_002dlocking>`_
   * - Turn on non-stop mode
     - ``set non-stop on``
     - `Non-stop mode <../ROCgdb/gdb/doc/gdb/Non_002dStop-Mode.html>`_. Run this before ``run`` or before you attach.
   * - Turn on all-stop mode
     - ``set non-stop off``
     - `All-stop mode <../ROCgdb/gdb/doc/gdb/All_002dStop-Mode.html>`_. Run this before ``run`` or before you attach.

Manage breakpoints, watchpoints, and catchpoints
------------------------------------------------

Use these commands to turn off, turn on, or remove the breakpoints, watchpoints, and catchpoints that you set. Run ``info breakpoints`` to list their numbers. ``<breakpoint-numbers>`` is one or more numbers or ranges, for example ``4`` or ``2-5``.

.. list-table::
   :header-rows: 1
   :widths: 35 30 35

   * - Task
     - Command
     - Example
   * - Disable
     - ``disable <breakpoint-numbers>``
     - ``disable 4``
   * - Enable
     - ``enable <breakpoint-numbers>``
     - ``enable 4``
   * - Delete
     - ``delete <breakpoint-numbers>``
     - ``delete 4``

Step and resume
---------------

Use these commands to move through the program one step at a time or to resume it.

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Task
     - Command
     - Notes
   * - Step one source line
     - ``step``, ``next``
     - ``step`` enters called functions. ``next`` steps over them.
   * - Step several source lines
     - ``step <count>``, ``next <count>``
     - For example, ``step 3``.
   * - Continue until a later source line
     - ``until``
     - Runs until a line after the current one, so you don't step through a loop more than once.
   * - Continue until an address
     - ``until *<address>``
     - For example, ``until *0x0000ffffdeadbeef``.
   * - Run until the current frame returns
     - ``finish``
     - Stops when the current function returns to its caller.
   * - Step one machine instruction
     - ``stepi``, ``nexti``
     - ``stepi`` enters called functions. ``nexti`` steps over them.
   * - Resume execution
     - ``continue``
     - Runs until the next breakpoint or the end of the program.

To run commands automatically when a breakpoint is hit, use a command sequence:

.. code-block:: shell

    (gdb) break <file>:<line-number>
    (gdb) commands <breakpoint-number>
    > continue
    > end

Can't find a command?
=====================

* For the AMD GPU commands and the debugging model, see `Debugging on AMD GPU <../ROCgdb/gdb/doc/gdb/AMD-GPU.html>`_ in the ROCgdb user guide.
* For every GDB command, see the `full user guide <../ROCgdb/gdb/doc/gdb/index.html>`_.
* The user guide is also installed with ROCm as an Info file at ``/opt/rocm/share/info/rocgdb/gdb.info`` (read it with ``info -f <path>``), along with the ROCgdb man pages.
* If a command or sample on this page is wrong or missing, `open an issue <https://github.com/ROCm/ROCgdb/issues>`_.
