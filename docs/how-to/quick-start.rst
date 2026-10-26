.. meta::
   :description: Source-level debugger for Linux based on the GNU Debugger
   :keywords: ROCgdb quick start, AMD ROCm Debugger quick start

.. _rocgdb-quick-start:

*********************
ROCgdb quick start
*********************

After :ref:`installing ROCgdb <rocgdb-installation>`, work through :ref:`rocgdb-first-hip-kernel`. It covers compiling with debug information, launching your application under ROCgdb, setting a kernel breakpoint, and selecting a wave and lane.

This page covers what the tutorial doesn't: attaching to a running process, switching layouts, and finding the full ROCgdb user guide.

Attach to a running process
===========================

To attach the debugger to a running process and continue execution, use:

.. code-block:: shell

   $ rocgdb -pid <process_id>
   […]
   (gdb) continue

Use the ``ps`` command to get the ``<process_id>`` of the application to attach to.

Switch layouts
==============

Switch layouts to suit the situation while you debug:

.. code-block:: shell

   layout src
   layout asm

The ``src`` layout is the source code view, and the ``asm`` layout is the assembly view. For more layouts, see `TUI-specific commands <https://rocm.docs.amd.com/projects/ROCgdb/en/latest/ROCgdb/gdb/doc/gdb/TUI-Commands.html>`_.

After you launch or attach, use the :ref:`rocgdb-essential-commands` to inspect and control your application.

ROCgdb user guide
=================

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
