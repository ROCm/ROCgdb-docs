---
myst:
  html_meta:
    "description lang=en": "Debug your first HIP kernel with ROCgdb. Compile with debug information, stop in a GPU kernel, select a wave and lane, inspect a value, and continue execution."
    "keywords": "ROCgdb tutorial, debug HIP kernel, first kernel breakpoint, wave, lane, saxpy"
---

(rocgdb-first-hip-kernel)=

# Debug your first HIP kernel

On this page, you build a {term}`HIP` application with debug information, then in one ROCgdb session stop inside a GPU {term}`kernel`, select a {term}`wave` and a {term}`lane`, print a value, and resume execution. You don't need the GDB manual to finish this page.

## When to use this page

Use this page when you can build and run a HIP application but have never stopped inside a kernel with ROCgdb, or when you want a known-good path before you debug your own code.

:::{note}
Each ROCgdb concept, such as a GPU wave appearing as a GDB thread, is explained in the step that uses it. For the full model, see {ref}`rocgdb-gpu-execution-state`.
:::

## Prerequisites

* ROCgdb is installed and on your `PATH`. See {ref}`rocgdb-installation`.
* Your system has a {ref}`supported AMD GPU <rocgdb-kl-supported>`.
* You have the [saxpy](https://github.com/ROCm/rocm-examples/tree/amd-staging/HIP-Basic/saxpy) example from the ROCm examples repository. The commands on this page assume the `saxpy` example directory, where the kernel is named `saxpy_kernel`:

  ```shell
  $ git clone https://github.com/ROCm/rocm-examples.git
  $ cd rocm-examples/HIP-Basic/saxpy
  ```

* Your system can build and run HIP applications without the debugger.

(rocgdb-first-hip-kernel-build)=

## 1. Compile with debug information

Build the HIP application so that source lines and variables are available to the debugger. The `-ggdb` option adds debug information, so ROCgdb can map machine code back to your source lines and variables. The `-O0` option turns off optimization, so the compiler doesn't reorder code or remove variables that you want to inspect. The `--offload-arch=native` option builds GPU code for the GPU in this system. The `-I` option points to the example's shared header.

```shell
$ amdclang++ -ggdb -O0 -x hip --offload-arch=native -I../../Common main.hip -o saxpy
```

If you build with `hipcc`, use the same options: `hipcc -ggdb -O0 -I../../Common main.hip -o saxpy`.

**Expected result:** The `saxpy` binary exists and still runs: `./saxpy` prints the usual host-side result.

:::{admonition} If this fails

Fix the HIP build first. If you omit `-ggdb` or build above `-O0`, later steps show `<optimized out>` values or no source lines.
:::

## 2. Launch ROCgdb

Start the binary under the debugger. The process isn't running yet; you get a `(gdb)` prompt.

```shell
$ rocgdb ./saxpy
```

**Expected result:** ROCgdb reads symbols from `./saxpy` and shows the `(gdb)` prompt.

## 3. Set a kernel breakpoint

The process hasn't started yet, so ROCgdb hasn't seen any GPU code. By default, the HIP runtime loads it only when the first kernel launches. Allow a pending breakpoint, so ROCgdb sets it when the code loads. Set the breakpoint by kernel function name, because a source-line breakpoint can resolve to the wrong place until the GPU code is loaded.

```shell
(gdb) set breakpoint pending on
(gdb) break saxpy_kernel
```

**Expected result:** ROCgdb reports that it can't find the function yet and that the breakpoint is pending:

```text
Function "saxpy_kernel" not defined.
Breakpoint 1 (saxpy_kernel) pending.
```

`info breakpoints` lists the breakpoint with `<PENDING>` as its address until the kernel's code is loaded.

:::{admonition} If this fails

If you run `break saxpy_kernel` without `set breakpoint pending on`, ROCgdb asks `Make breakpoint pending on future shared library load? (y or [n])`. If you answer `n`, no breakpoint is created and the kernel never stops. See {ref}`rocgdb-troubleshoot-breakpoint-not-hit`.
:::

## 4. Run the application

Start the application. It runs until a wave reaches the kernel breakpoint.

```shell
(gdb) run
```

**Expected result:** Execution stops inside `saxpy_kernel`, and ROCgdb reports an AMDGPU wave.

:::{admonition} If this fails

If the application runs to completion without stopping, check debug symbols, breakpoint resolution, and whether the kernel launched. A {ref}`supported AMD GPU <rocgdb-kl-supported>` must be visible to the application. If it isn't, the application exits with a HIP error before it launches the kernel. See {ref}`rocgdb-troubleshoot-breakpoint-not-hit`.
:::

(rocgdb-first-hip-kernel-select-wave)=

## 5. Select a wave

ROCgdb represents a GPU wave through GDB's thread abstraction. List the threads, then select the wave you want to inspect.

```shell
(gdb) info threads
```

Sample output. This sample is illustrative, not captured from a real run. The IDs, addresses, paths, and line numbers differ on your system:

```text
  Id   Target Id                                     Frame
  1    Thread 0x7ffff6288180 (LWP 645917) "saxpy" 0x00007ffff207d586 in ?? () from /opt/rocm/lib/libhsa-runtime64.so.1
  2    Thread 0x7fffe81ff6c0 (LWP 645924) "saxpy" __GI___ioctl (fd=3, request=3222817548) at ../sysdeps/unix/sysv/linux/ioctl.c:36
* 7    AMDGPU Wave 1:2:1:1 (0,0,0)/0 "saxpy"      saxpy_kernel () at main.hip:8
```

Select a wave by its ID:

```shell
(gdb) thread <wave-thread-id>
```

**Expected result:** The `AMDGPU Wave` entry is marked with `*` as the current thread.

## 6. Select a lane

A wave runs many {term}`work-items <work-item>` in lockstep. ROCgdb calls the position of each work-item in the wave a lane. List the lanes of the selected wave, then select one.

```shell
(gdb) info lanes
```

Sample output. This sample is illustrative, like the previous one:

```text
  Id   State Target Id                            Frame
* 0    A     AMDGPU Lane 1:2:1:1/0 (0,0,0)[0,0,0] saxpy_kernel () at main.hip:8
```

```shell
(gdb) lane <lane-id>
```

**Expected result:** The selected context identifies one wave and one lane.

(rocgdb-first-hip-kernel-inspect-value)=

## 7. Inspect a value

The breakpoint stopped the wave at the start of the kernel, before it computes `global_idx`. Delete the breakpoint so that other waves don't stop while you step, run the line that computes `global_idx`, then print variables in the context of the selected wave and lane:

```shell
(gdb) delete 1
(gdb) next
(gdb) print global_idx
(gdb) print d_x[global_idx]
```

Each `print` command prints a value in the form `$<n> = <value>`.

**Expected result:** `global_idx` is the selected lane's index in the grid, `blockIdx.x * blockDim.x + threadIdx.x`, and `d_x[global_idx]` is `global_idx + 1`, because the example fills `x` with `1, 2, 3, ...`. Select a different lane with `lane <lane-id>` and print again to see both values change.

:::{admonition} If this fails

If a variable is unavailable or optimized out, verify the optimization level (`-O0`), the variable scope, and the selected lane.
:::

## 8. Continue

Resume all waves. You deleted the breakpoint in step 7, so the application runs to the end.

```shell
(gdb) continue
```

**Expected result:** The application prints its result, and ROCgdb reports `[Inferior 1 (process <process-id>) exited normally]`. To end the session, run `quit`.

If you continue without deleting the breakpoint, every wave that reaches it stops, so ROCgdb stops again in another wave each time.

## You are done when

You have stopped in GPU code, selected a wave and a lane, inspected data for that lane, and resumed execution.

## Related information

* {ref}`GPU execution state in ROCgdb <rocgdb-gpu-execution-state>`
* {ref}`Kernel breakpoint isn't hit <rocgdb-troubleshoot-breakpoint-not-hit>`
* {ref}`Commands by task <rocgdb-essential-commands>`
