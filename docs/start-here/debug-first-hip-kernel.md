---
myst:
  html_meta:
    "description lang=en": "Debug your first HIP kernel with ROCgdb. Compile with debug information, stop in a GPU kernel, select a wave and lane, inspect a value, and continue execution."
    "keywords": "ROCgdb tutorial, debug HIP kernel, first kernel breakpoint, wave, lane, saxpy"
---

% TODO(engineering validation): Confirm the expected-result statements on
% this page against a supported ROCm and ROCgdb release before publication.
% Replace the sample `info threads` and `info lanes` output with output from
% the saxpy example (kernel name, source file, and program name), and add
% real output to the expected result in step 4.

(rocgdb-first-hip-kernel)=

# Debug your first HIP kernel

In one session, you build a HIP application with debug information, stop inside a GPU kernel, select a wave and a lane, print a value, and resume execution. You don't need the GDB manual to finish this page.

## When to use this page

Use this page when you can build and run a HIP application but have never stopped inside a kernel with ROCgdb, or when you want a known-good path before you debug your own code.

:::{note}
This page assumes you can compile and run `saxpy`. It explains the ROCgdb ideas, such as a GPU wave appearing as a GDB thread, where you use them. For the full model, see {ref}`rocgdb-gpu-execution-state`.
:::

## Prerequisites

* ROCgdb is installed and on your `PATH`. See {ref}`rocgdb-installation`.
* You have the [saxpy](https://github.com/ROCm/rocm-examples/tree/amd-staging/HIP-Basic/saxpy) example from the ROCm examples repository, or an equivalent one-kernel HIP program. The commands on this page assume the `saxpy` example directory, where the kernel is named `saxpy_kernel`.
* The application runs without the debugger.

## 1. Compile with debug information

Build so that source lines and variables are available to the debugger. The `-I` option points to the example's shared header. With amd-llvm, use `amdclang++ -ggdb -O0 -x hip --offload-arch=native -I../../Common main.hip -o saxpy` instead.

```shell
$ hipcc -ggdb -O0 -I../../Common main.hip -o saxpy
```

:::{admonition} Expected result
:class: rocgdb-expected

The `saxpy` binary exists and still runs: `./saxpy` prints the usual host-side result.
:::

:::{admonition} If this fails
:class: rocgdb-iffails

Fix the HIP build first. If you omit `-ggdb` or use a high `-O` level, later steps look like debugger bugs.
:::

## 2. Launch ROCgdb

Start the binary under the debugger. The process isn't running yet; you get a `(gdb)` prompt.

```shell
$ rocgdb ./saxpy
```

:::{admonition} Expected result
:class: rocgdb-expected

ROCgdb reads symbols from `./saxpy` and shows the `(gdb)` prompt.
:::

## 3. Set a kernel breakpoint

By default, the HIP runtime loads GPU code only when the first kernel launches. Before then, ROCgdb can't find the kernel, so you must allow a pending breakpoint. Set the breakpoint by kernel function name, because a source-line breakpoint can resolve to the wrong place until the GPU code is loaded.

```shell
(gdb) set breakpoint pending on
(gdb) break saxpy_kernel
```

:::{admonition} Expected result
:class: rocgdb-expected

ROCgdb reports that it can't find the function yet and that the breakpoint is pending:

```shell
Function "saxpy_kernel" not defined.
Breakpoint 1 (saxpy_kernel) pending.
```

`info breakpoints` lists the breakpoint with `<PENDING>` as its address until the kernel's code is loaded.
:::

:::{admonition} If this fails
:class: rocgdb-iffails

If you run `break saxpy_kernel` without `set breakpoint pending on`, ROCgdb asks `Make breakpoint pending on future shared library load? (y or [n])`. If you answer `n`, no breakpoint is created and the kernel never stops. See {ref}`rocgdb-troubleshoot-breakpoint-not-hit`.
:::

## 4. Run the application

```shell
(gdb) run
```

:::{admonition} Expected result
:class: rocgdb-expected

Execution stops inside `saxpy_kernel`, and ROCgdb reports an AMDGPU wave.
:::

:::{admonition} If this fails
:class: rocgdb-iffails

If the application runs to completion without stopping, check debug symbols, breakpoint resolution, and whether the kernel launched. A ROCm-capable GPU must be visible to the application. If it isn't, the application exits with a HIP error before it launches the kernel. See {ref}`rocgdb-troubleshoot-breakpoint-not-hit`.
:::

## 5. Select a wave

ROCgdb represents a GPU wave through GDB's thread abstraction. List the threads, then select the wave you want to inspect.

```shell
(gdb) info threads
```

Sample output. The kernel name, IDs, addresses, and paths differ on your system:

```shell
  Id   Target Id                                     Frame
  1    Thread 0x7ffff6288180 (LWP 645917) "saxpy" 0x00007ffff207d586 in ?? () from /opt/rocm-7.1.0/lib/libhsa-runtime64.so.1
  2    Thread 0x7fffe81ff6c0 (LWP 645924) "saxpy" __GI___ioctl (fd=3, request=3222817548) at ../sysdeps/unix/sysv/linux/ioctl.c:36
* 7    AMDGPU Wave 1:2:1:1 (0,0,0)/0 "saxpy"      saxpy_kernel () at main.hip:8
```

Select a wave by its ID:

```shell
(gdb) thread <wave-thread-id>
```

:::{admonition} Expected result
:class: rocgdb-expected

The `AMDGPU Wave` entry is marked with `*` as the current thread.
:::

## 6. Select a lane

A wave runs many work-items in lockstep. ROCgdb calls each work-item a lane. List the lanes of the selected wave, then select one.

```shell
(gdb) info lanes
```

Sample output:

```shell
  Id   State Target Id                            Frame
* 0    A     AMDGPU Lane 1:2:1:1/0 (0,0,0)[0,0,0] saxpy_kernel () at main.hip:8
```

```shell
(gdb) lane <lane-id>
```

:::{admonition} Expected result
:class: rocgdb-expected

The selected context identifies one wave and one lane.
:::

## 7. Inspect a value

Print variables in the context of the selected wave and lane.

```shell
(gdb) print global_idx
(gdb) print d_y[global_idx]
```

Each command prints a value in the form `$<n> = <value>`.

:::{admonition} Expected result
:class: rocgdb-expected

The values correspond to the lane you selected. Select a different lane and print again to see them change.
:::

:::{admonition} If this fails
:class: rocgdb-iffails

If a variable is unavailable or optimized out, verify the optimization level (`-O0`), the variable scope, and the selected lane.
:::

## 8. Continue

```shell
(gdb) continue
```

ROCgdb might stop again when another wave reaches the breakpoint.

To end the session, run `quit`.

## You are done when

You have stopped in GPU code, selected a wave and a lane, inspected data for that lane, and resumed execution.

## Related information

* {ref}`Understand GPU execution state <rocgdb-gpu-execution-state>`
* {ref}`Troubleshoot a kernel breakpoint that isn't hit <rocgdb-troubleshoot-breakpoint-not-hit>`
* {ref}`Commands by task <rocgdb-essential-commands>`
