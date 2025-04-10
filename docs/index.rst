.. meta::
   :description: Source-level debugger for Linux based on the GNU Debugger
   :keywords: ROCgdb documentation, AMD ROCm Debugger documentation

.. _index:

===========================
ROCgdb documentation
===========================

The AMD ROCm Debugger (ROCgdb) is the AMD source-level debugger for Linux,
based on the `GNU Debugger (GDB) <https://www.sourceware.org/gdb/documentation/>`_. ROCgdb enables heterogeneous debugging on the ROCm software that consists of an x86-based host architecture along with
commercially available AMD GPU architectures supported by the :doc:`AMD Debugger API
Library (ROCdbgapi) <rocdbgapi:index>`. ROCdbgapi is included with ROCm.

ROCgdb provides the following features:

- Debugs ROCm applications running on actual hardware
- Debugs applications without the potential variations introduced by simulation and emulation environments
- Offers a seamless debugging environment that allows simultaneous GPU and CPU code debugging within the same application, just like programming in HIP, which is a seamless extension of C++ programming
- Additional features to support debugging ROCm device code on top of the existing GDB debugging features, which are inherently present for debugging the host code
- Supports :doc:`HIP <hip:index>` kernel debugging
- Allows you to set breakpoints, single-step ROCm applications, and inspect and modify the memory and variables of any given thread running on the hardware

.. note::
    The current version of ROCgdb is an initial prototype that focuses on source line debugging and doesn't support symbolic variable debugging capabilities.

The code is open source and hosted at: https://github.com/ROCm/ROCgdb

.. grid:: 2
  :gutter: 3

  .. grid-item-card:: Install

    * :ref:`installation`

  .. grid-item-card:: How to

    * :ref:`rocgdb-quick-start`

    * |ROCgdb user guide|

To contribute to the documentation, refer to
`Contributing to ROCm  <https://rocm.docs.amd.com/en/latest/contribute/contributing.html>`_.

You can find licensing information on the `Licensing <https://rocm.docs.amd.com/en/latest/about/license.html>`_ page.

.. |ROCgdb user guide| raw:: html

   <a href="ROCgdb/gdb/doc/gdb/index.html" target="_blank">ROCgdb user guide</a>
