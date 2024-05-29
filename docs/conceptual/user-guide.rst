.. meta::
   :description: Source-level debugger for Linux, based on the GNU Debugger
   :keywords: ROCgdb, ROCm, library, API, tool

.. _user-guide:

========================
User guide
========================

You can use the standard GNU debugger (GDB) commands for both CPU and GPU code debugging. 
Here is the |ROCgdb user guide| that provides information about using ROCgdb. This user guide is also installed in the following directories when you `install ROCm <https://rocm.docs.amd.com/projects/install-on-linux/en/latest/>`_:

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

For more information on GDB, visit the official page of `GNU Debugger <http://www.gnu.org/software/gdb>`_.

.. |ROCgdb user guide| raw:: html

   <a href="../ROCgdb/gdb/doc/gdb/index.html" target="_blank">ROCgdb debugger manual</a>
