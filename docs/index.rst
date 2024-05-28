.. meta::
   :description: Source-level debugger for Linux, based on the GNU Debugger
   :keywords: ROCgdb, ROCm, library, API, tool

.. _index:

===========================
ROCgdb documentation
===========================

The AMD ROCm Debugger (ROCgdb) is the AMD source-level debugger for Linux,
based on the GNU Debugger (GDB). ROCgdb enables heterogeneous debugging on the
ROCm software that comprises of an x86-based host architecture along with
commercially available AMDGPU architectures supported by the AMD Debugger API
Library (ROCdbgapi). ROCdbgapi is included with the ROCm release.

.. note::
    The current version of ROCgdb is an initial prototype that focuses on source line debugging and doesn't support symbolic variable debugging capabilities.

You can access ROCgdb code on our `<https://github.com/ROCm/ROCgdb>`_.

.. grid:: 2
  :gutter: 3

  .. grid-item-card:: Install

    * :ref:`installation`

The documentation is structured as follows:
    
.. grid:: 2
  :gutter: 3

  .. grid-item-card:: Tutorials

    * :ref:`tutorial`

  .. grid-item-card:: Conceptual

    * :ref:`user-guide`

  .. grid-item-card:: Reference

    * |ROCgdb user guide|
         
To contribute to the documentation, refer to
`Contributing to ROCm  <https://rocm.docs.amd.com/en/latest/contribute/contributing.html>`_.

You can find licensing information on the `Licensing <https://rocm.docs.amd.com/en/latest/about/license.html>`_ page.

.. |ROCgdb user guide| raw:: html

   <a href="ROCgdb/gdb/doc/gdb/index.html" target="_blank">ROCgdb Documentation</a>
