.. meta::
   :description: Source-level debugger for Linux based on the GNU Debugger
   :keywords: ROCgdb commands, AMD ROCm Debugger quick start, ROCgdb quick reference

.. _rocgdb-essential-commands:

***********************************
ROCgdb commands for key operations
***********************************

This topic summarizes the ROCgdb commands for key operations.

Inspecting kernel state
========================

Here are the commands used to inspect the kernel state:

View kernel code
-----------------

.. code-block:: shell

    (gdb) list

Sample output:

.. code-block:: shell

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

View disassembly
-----------------

.. code-block:: shell

    (gdb) disassemble

Sample output:

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

View system information
------------------------

- **Agents:**

  .. code-block:: shell

    (gdb) info agents

  Sample output:

  .. code-block:: shell

      Id State Target Id                  Architecture Device Name        Cores Threads Location
    * 1  A     AMDGPU Agent (GPUID 35090) gfx90a       AMD Instinct MI210 416   3328    0000:4a:00.0
      2  A     AMDGPU Agent (GPUID 34915) gfx90a       AMD Instinct MI210 416   3328    0000:09:00.0
      3  A     AMDGPU Agent (GPUID 56224) gfx90a       AMD Instinct MI210 416   3328    0000:0c:00.0
      4  A     AMDGPU Agent (GPUID 33385) gfx90a       AMD Instinct MI210 416   3328    0000:11:00.0

- **Queues:**

  .. code-block:: shell

    (gdb) info queues

  Sample output:

  .. code-block:: shell

      Id   Target Id                Type         Read   Write  Size     Address
      1    AMDGPU Queue 1:1 (QID 0) HSA          2      2      4096     0x00007ffff626e000
    * 2    AMDGPU Queue 1:2 (QID 1) HSA          0      2      1048576  0x00007fffe5800000

- **Dispatches:**

  .. code-block:: shell

    (gdb) info dispatches

  Sample output:

  .. code-block:: shell

     Id   Target Id                      Grid    Workgroup Fence   Kernel Function
    * 1    AMDGPU Dispatch 1:2:1 (PKID 0) [1,1,1] [1,1,1]   B|Aa|Ra kern()

- **Threads:**

  .. code-block:: shell

    (gdb) info threads

  Sample output:

  .. code-block:: shell

      Id   Target Id                                     Frame
      1    Thread 0x7ffff6288180 (LWP 645917) "nosimple" 0x00007ffff207d586 in ?? () from /opt/rocm-7.1.0/lib/libhsa-runtime64.so.1
      2    Thread 0x7fffe81ff6c0 (LWP 645924) "nosimple" __GI___ioctl (fd=3, request=3222817548) at ../sysdeps/unix/sysv/linux/ioctl.c:36
      4    Thread 0x7fffe61ff6c0 (LWP 645926) "nosimple" __GI___ioctl (fd=3, request=3222817548) at ../sysdeps/unix/sysv/linux/ioctl.c:36
      6    Thread 0x7ffff5fff6c0 (LWP 645930) "nosimple" __GI___ioctl (fd=3, request=3222817548) at ../sysdeps/unix/sysv/linux/ioctl.c:36
    * 7    AMDGPU Wave 1:2:1:1 (0,0,0)/0 "saxpy"      kern () at /home/user/saxpy.cpp:7

- **Lanes:**

  .. code-block:: shell

    (gdb) info lanes

  Sample output:

  .. code-block:: shell

      Id   State Target Id                            Frame
    * 0    A     AMDGPU Lane 1:2:1:1/0 (0,0,0)[0,0,0] kern () at /home/user/saxpy.cpp:7

View back trace
----------------

.. code-block:: shell

    (gdb) backtrace

Sample output:

.. code-block:: shell

    #0  saxpy (tid=0) at /home/oogunbow/saxpy.cpp:33
    #1  0x00007ffff608ee40 in kern () at /home/user/saxpy.cpp:4

View stack frames
------------------

.. code-block:: shell

    (gdb) info frame

Sample output:

.. code-block:: shell

    Stack level 0, frame at private_wave#0x800:
    pc = 0x7ffff608e3bc in bar (/home/user/saxpy.cpp:33); saved pc = 0x7ffff608ee40
    called by frame at private_wave#0x0
    source language c++.
    Arglist at private_wave#0x800, args: tid=0
    Locals at private_wave#0x800, Saved registers:
    v36 at private_wave#0x1500, v37 at private_wave#0x1600

View frame arguments
---------------------

.. code-block:: shell

    (gdb) info args

Sample output:

.. code-block:: shell

    tid = 0

View frame local variables
---------------------------

.. code-block:: shell

    (gdb) info locals

Sample output:

.. code-block:: shell

    No locals.

View GPU registers
-------------------

.. code-block:: shell

    (gdb) info registers

This command dumps the content of the current wavefront's registers.

Sample output:

.. code-block:: shell

    v0             {0x30 <repeats 64 times>}
    ....
    s41            0x0                 0
    m0             0x1008              4104
    pc             0x7ffff608e3bc      0x7ffff608e3bc <saxpy(int)+268>
    exec           0x5555555555555555  6148914691236517205
    vcc            0xffffffffffffffff  18446744073709551615

This command dumps only the general-purpose registers, which provide all-inclusive data about the state of the current wavefront.

To get data for all registers, use:

.. code-block:: shell

    (gdb) info all-registers

View GPU data @ address spaces
-------------------------------

.. code-block:: shell

    (gdb) x/nfu global#0xdeadbeef
    (gdb) x/nfu local#0xdeadbeef
    (gdb) x/nfu generic#0xdeadbeef
    (gdb) x/nfu private_wave#0xdeadbeef
    (gdb) x/nfu private_lane#0xdeadbeef

View CPU/GPU threads
---------------------

.. code-block:: shell

    (gdb) info threads

Sample output:

.. code-block:: shell

      Id   Target Id                                    Frame
      1    Thread 0x7ffff648bf80 (LWP 1981864) "saxpy" 0x00007ffff5a6c9ef in ?? () from /opt/rocm-7.1.0/lib/libhsa-runtime64.so.1
      2    Thread 0x7ffff55ff6c0 (LWP 1981871) "saxpy" __GI___ioctl (fd=3, request=3222817548) at ../sysdeps/unix/sysv/linux/ioctl.c:36
      4    Thread 0x7fffeffff6c0 (LWP 1981873) "saxpy" __GI___ioctl (fd=3, request=3222817548) at ../sysdeps/unix/sysv/linux/ioctl.c:36
      6    Thread 0x7ffff5dff6c0 (LWP 1981877) "saxpy" __GI___ioctl (fd=3, request=3222817548) at ../sysdeps/unix/sysv/linux/ioctl.c:36
    * 7    AMDGPU Wave 1:2:1:1 (0,0,0)/0 "saxpy"       saxpy_kernel () at saxpy.cpp:8

Switch threads
---------------

.. code-block:: shell

    (gdb) thread <id>

Printing kernel data
=====================

Commands to print the kernel data:

Print variable
---------------

.. code-block:: shell

    (gdb) print foo

Print array
------------

.. code-block:: shell

    (gdb) print *foo[2]@8     -- i.e. (gbb) print *<address>@<count>

Print expressions
------------------

.. code-block:: shell

    (gdb) print foo[4] >> 1

Print formats
--------------

.. code-block:: shell

    // (gdb) p/<code> <value>
    (gdb) p/x foo[1]

The values for <code> are:

- x - hexadecimal
- d - decimal
- u - unsigned decimal
- o - octal
- t - binary (two)
- a - address (hex + offset)
- c - character
- f - float
- s - string
- z - hexadecimal with leading zeros
- r - raw (skips pretty printing)

Modifying kernel data
======================

The commands to modify the kernel data:

Using set command
------------------

Use the ``set`` command to modify kernel data directly.

.. code-block:: shell

    (gdb) set var foo[1]=45

Using print command
--------------------

The ``print`` command is an indirect way to modify the kernel data.

.. code-block:: shell

    (gdb) print foo[3]=3

Changing kernel focus
======================

Commands to change the kernel thread, lane, or frame:

Change thread
--------------

.. code-block:: shell

    (gdb) thread 9

Change lane
------------

.. code-block:: shell

    (gdb) lane 5

Change frame
-------------

.. code-block:: shell

    (gdb) frame <index>
    (gdb) up <count>
    (gdb) down <count>

Controlling kernel execution
=============================

Commands to control kernel execution:

Set breakpoints
----------------

.. code-block:: shell

    (gdb) break saxpy.cpp:47
    (gdb) break func_foo
    (gdb) break *0x01234567

Set temporary breakpoints
--------------------------

.. code-block:: shell

    (gdb) tbreak saxpy.cpp:47
    (gdb) tbreak func_foo
    (gdb) tbreak +24

Set conditional breakpoints
----------------------------

.. code-block:: shell

    (gdb) break func_foo if idx == 9
    (gdb) break func_foo if $_agent == 2
    (gdb) break func_foo if $_queue == 1
    (gdb) break func_foo if $_dispatch == 6
    (gdb) break func_foo if $_thread == 7
    (gdb) break func_foo if $_lane == 15
    (gdb) break func_foo if $_thread_workgroup_pos == 3
    (gdb) break func_foo if $_lane_workgroup_pos == "[0,0,0]"

Set watchpoints
----------------

.. code-block:: shell

    (gdb) watch foo[4]

Set catchpoints
----------------

.. code-block:: shell

    (gdb) catch load            -- Catch loads of shared libraries (debug dynamic linking).
    (gdb) catch unload          -- Catch unloads of shared libraries (track cleanup/unloading).
    (gdb) catch rethrow         -- Catch an exception, when rethrown (trace exception propagation).
    (gdb) catch signal SIGSEGV  -- Catch signals by their names and/or numbers (debug crashes or signals).
    (gdb) catch syscall open    -- Catch system calls by names, groups, or numbers (trace system-level calls).
    (gdb) catch throw           -- Catch an exception, when thrown (trace exception origins).
    (gdb) catch vfork           -- Catch calls to vfork (monitor child process creation).

Set scheduler locking (waves)
------------------------------

.. code-block:: shell

    (gdb) set scheduler-locking on

Set scheduler non-stop (waves)
-------------------------------

.. code-block:: shell

    set non-stop non

Set scheduler all-stop (waves)
-------------------------------

.. code-block:: shell

    set non-stop off

Disable breakpoint, watchpoint, catchpoint
-------------------------------------------

.. code-block:: shell

    disable 4

Enable breakpoint, watchpoint, catchpoint
------------------------------------------

.. code-block:: shell

    enable 4

Delete breakpoint, watchpoint, catchpoint
------------------------------------------

.. code-block:: shell

    // delete <list>
    delete 4

Step execution (source line)
-----------------------------

.. code-block:: shell

    (gdb) step
    (gdb) next

Step execution (multiple source lines)
---------------------------------------

.. code-block:: shell

    (gdb) step 3
    (gdb) next 3

Step execution (stack frame)
-----------------------------

.. code-block:: shell

    (gdb) until
    (gdb) until 0x0000ffffdeadbeef
    (gdb) finish

Step execution (machine instruction)
-------------------------------------

.. code-block:: shell

    (gdb) stepi
    (gdb) nexti

Resume execution
-----------------

.. code-block:: shell

    (gdb) continue

**Command sequence:**

.. code-block:: shell

    (gdb) break saxpy.cpp:47
    command BREAKPOINT_NUMBER
    continue
    end
