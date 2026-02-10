.. meta::
   :description: Source-level debugger for Linux based on the GNU Debugger
   :keywords: Install GDB TUI, AMD ROCm Debugger installation, ROCgdb TUI installation

.. _install-gdb-tui:

*****************************
Installing GDB dashboard TUI
*****************************

`GDB dashboard <https://github.com/cyrus-and/gdb-dashboard>`_ is a standalone ``.gdbinit`` file written using the `Python API <https://sourceware.org/gdb/onlinedocs/gdb/Python-API.html>`_, that enables a modular interface showing relevant information about the program being debugged.

Installation
=============

To install the GDB dashboard, download the `.gdbinit file <https://raw.githubusercontent.com/cyrus-and/gdb-dashboard/master/.gdbinit>`_ and place in your home directory.

Layout setup
=============

During debugging, the default dashboard layout setup appears automatically every time the inferior program stops. The purpose of GDB dashboard is to reduce the number of GDB commands needed to inspect the status of current program thus allowing the developer to primarily focus on the control flow.

To display the default set of views, use this command:

.. code-block:: shell

    (gdb) dashboard -layout

**Sample output:**

.. code-block:: shell

    Dashboard    (default TTY)
    assembly     (default TTY)
    breakpoints  (default TTY)
    expressions  (default TTY)
    history      (default TTY)
    memory       (default TTY)
    registers    (default TTY)
    source       (default TTY)
    stack        (default TTY)
    threads      (default TTY)
    variables    (default TTY)

Customizing the dashboard
==========================

The GDB dashboard TUI is very customizable. You can customize the TUI to eliminate the less-commonly used views from the default display during a debug session, such as **Expressions**, **History**, and **Memory**.

To avoid a cluttered display with a lot of AMD GPU registers displaying constantly on the dashboard, you can elide the **Register** view from the default dashboard using the following commands:

.. code-block:: shell

    (gdb) dashboard registers
    registers module disabled
    (gdb) dashboard expressions
    expressions module disabled
    (gdb) dashboard history
    history module disabled
    (gdb) dashboard memory
    memory module disabled

Here is how compact the customized dashboard will look:

.. image:: /data/gdb-tui-layout-setup.png
   :width: 100%
   :align: center

Furthermore, the dashboard offers a number of stylable attributes that can be modified via the ``-style`` command, which applies to both the dashboard and individual modules. For example, the height of the Source view can be increased using the following command:

.. code-block:: shell

    (gdb) dashboard source -style height 35

Dashboard command-line options
===============================

The following table lists the ``dashboard`` command-line options:

.. list-table:: dashboard cli options
    :header-rows: 1

    * - Option
      - Description

    * - ``configuration``
      - Dumps or saves the dashboard configuration.

    * - ``enabled``
      - Enables or disables the dashboard.

    * - ``layout``
      - Sets or shows the dashboard layout.

    * - ``output``
      - Sets the output file or TTY for the whole dashboard or individual module.

    * - ``style``
      - Configures the stylable attributes.

    * - ``assembly``
      - Configures the assembly module. Using without arguments toggles its visibility.

    * - ``breakpoints``
      - Configures the breakpoints module. Using without arguments toggles its visibility.

    *



