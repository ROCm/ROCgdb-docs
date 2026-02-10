.. meta::
   :description: Source-level debugger for Linux based on the GNU Debugger
   :keywords: Install VS code GUI, AMD ROCm Debugger GUI, ROCgdb Visual studio code GUI

.. _setting-vsc-gui:

************************
Setting up VS Code GUI
************************

This topic provides information on configuring Visual Studio (VS) Code GUI for debugging applications using ROCgdb.

Installing extensions
======================

To use ROCgdb within the VS Code, you need to install some VS Code extensions. Only two extensions are required from external vendors while the rest are provided by Microsoft. These extensions are grouped into three categories:

- Must-have extensions. These are required for HIP debugging.

- Extra extensions for Python tracing.

- Optional extensions.

Must-have extensions
---------------------

- C/C++ for VS Code by Microsoft

- C/C++ for Extension Pack by Microsoft

- C/C++ Themes by Microsoft

- Remote SSH by Microsoft

- Remote Explorer by Microsoft

- Remote Development by Microsoft

  - This installs Dev Containers and Remote Tunnels by Microsoft, which is necessary for tracing under Docker.

- Docker by Microsoft

Extra extensions for Python tracing
------------------------------------

- Pylance by Microsoft

- Python by Microsoft

- Python Debugger by Microsoft

- Python C++ Debugger by BeniBenj

.. note::

   VS Code requires you to install the extensions on the remote system as well.

Optional extensions
--------------------

- Jupiter by Microsoft

- GitHub Pull Request by Microsoft

Configuring the Remote Debugger settings
=========================================

After installing the VS Code extensions, you need to configure the Remote Debugger settings. The settings help VS Code to connect (Attach) to the machine hosting the HIP program to be debugged and execute the program under ROCgdb.

Follow these steps to configure the Remote Debugger settings:

1. Select **Remote Explorer** and add the new remote:

   - Add the ssh command line ``ssh amd@<mi300-system>.ctr.dcgpu``.

2. Connect to the remote system.

3. Open the repo folder on the remote system. You can use a previously cloned CLR repo from the public GitHub.

4. Click on **Run and Debug** button on the left panel.

5. Click on **Create a launch.json** file.

6. Select **GDB** in the drop out menu and add these two configurations: **(gdb) Attach** and **(gdb) Launch**.

   - Attach doesn't require any extra setup.

   - Launch requires the environment variable ``LD_LIBRARY_PATH`` to point to the debug build of runtime.

   - If required, set the Debugger path to ``rocgdb``. For example, ``miDebuggerPath: /opt/rocm-7.2.0/bin/rocgdb``.

Configuration file: launch.json
================================

The launch.json configuration file contains information required by VS Code to Launch or Attach to a program for debugging. This information includes path information for the Debugger and the program including the arguments and environment variables.

Here is a sample launch.json file:

.. code-block:: shell

   {
      "version": "0.2.0",
      "configurations": [
         {
            "name": "(gdb) Attach",
            "type": "cppdbg",
            "request": "attach",
            "processId": "${command:pickProcess}",
            "program" : "/usr/bin/python3",
            "miDebuggerPath": "/opt/rocm-6.4.0/bin/rocgdb",
            "MIMode": "gdb",
            "setupCommands": [
            {
               "description": "Enable pretty-printing for gdb",
               "text": "-enable-pretty-printing",
               "ignoreFailures": true
            },
            {
               "description": "Set Disassembly Flavor to Intel",
               "text": "-gdb-set disassembly-flavor intel",
               "ignoreFailures": true
            }
            ]
         },
         {
            "name": "(gdb) Launch",
            "type": "cppdbg",
            "request": "launch",
            "program": "/home/amd/german/graph/graph",
            "args": [
            "Unit_hipMemcpy_MultiThread-AllAPIs"
            ],
            "stopAtEntry": true,
            "cwd": "/home/amd/german/graph/",
            "environment": [
            {
               "name": "LD_LIBRARY_PATH",
               "value": "/home/amd/german/udp/clr/build/install/lib/:/opt/rocm/lib"
            },
            {
               "name": "DEBUG_HIP_MEM_POOL_VMHEAP",
               "value": "1"
            }
            ],
            "externalConsole": false,
            "MIMode": "gdb",
            "setupCommands": [
            {
               "description": "Enable pretty-printing for gdb",
               "text": "-enable-pretty-printing",
               "ignoreFailures": true
            },
            {
               "description": "Set Disassembly Flavor to Intel",
               "text": "-gdb-set disassembly-flavor intel",
               "ignoreFailures": true
            }
            ]
         }
      ]
   }

Launching the Debugger
=======================

After the Debugger settings are configured, the Run and Debug tab will show these two options:

- **(gdb) Attach option:** This option is used to connect the Debugger to a running process.

- **(gdb) Launch option:** This option is used to start a process under Debugger control.

To start remote debugging, follow these steps:

1. Click on the **Launch** option to start the application under Debugger control:

   - ``stopAtEntry: true`` stops the application on ``main()``.

2. Navigate in the repo and set breakpoints in the application or runtime source code.

3. VS Code enables pretty printers by default.

   - STL classes are easily modifiable like regular data sets.

   - ROCgdb might require ``~/.gdbinit`` for pretty printers:

     .. code-block:: shell

      python
      import sys
      sys.path.insert(0, '/usr/share/gcc/python')
      from libstdcxx.v6.printers import register_libstdcxx_printers
      register_libstdcxx_printers (None)
      end

4. ROCgdb also facilitates device kernel tracing. Breakpoints, variables, and registers work automatically.

Debugger displays
==================

During an active debug session, several tabs are available for displaying the running program and kernel states. These include tabs to display kernel variable, call stack frame, GPU registers, and source code breakpoint locations.

.. image:: /data/debugger_display.png
   :width: 100%
   :align: center

Debug console
==============

During a debug session when the inferior is stopped, you can enter ROCgdb commands in the Debug console. All such commands must be entered with a ``-exec`` prefix. For example, all GPU threads can be displayed using ``-exec info threads``.

.. image:: /data/debugger_display.png
   :width: 100%
   :align: center
