---
myst:
  html_meta:
    "description lang=en": "Troubleshoot a ROCgdb breakpoint in a HIP kernel that never stops. Check debug symbols, pending breakpoints, kernel launch, code loading, and GPU support."
    "keywords": "ROCgdb breakpoint not hit, kernel breakpoint, pending breakpoint, deferred loading, HIP_ENABLE_DEFERRED_LOADING"
---

(rocgdb-troubleshoot-breakpoint-not-hit)=

# Kernel breakpoint isn't hit

Find out why ROCgdb doesn't stop at a breakpoint in a HIP kernel.

## When to use this page

Use this page when your application runs to completion, or runs past the point where you expect it to stop, and ROCgdb never stops in your GPU kernel, or stops on a different line than you set. If you haven't stopped in a kernel before, start with {ref}`rocgdb-first-hip-kernel`.

Work through the steps in order. Each one rules out a common cause.

## Prerequisites

* ROCgdb is installed and on your `PATH`. See {ref}`rocgdb-installation`.
* The application runs correctly without the debugger.
* You can reproduce the problem in a ROCgdb session.
* The commands use the [saxpy example](https://github.com/ROCm/rocm-examples/tree/amd-staging/HIP-Basic/saxpy). Replace `main.hip`, `saxpy`, and `saxpy_kernel` with your own file, binary, and kernel names.

(rocgdb-bp-check-build)=

## 1. Confirm the build has debug information

If your build already uses `-ggdb -O0`, skip to {ref}`step 2 <rocgdb-bp-check-exists>`. Otherwise, rebuild with debug information (`-ggdb`) and no optimization (`-O0`), with `amdclang++` or `hipcc`, and start a new ROCgdb session.

```shell
$ amdclang++ -ggdb -O0 -x hip --offload-arch=native -I../../Common main.hip -o saxpy
```

**Expected result:** The rebuilt binary runs without the debugger, and in ROCgdb, `list main` shows source lines.

:::{admonition} If this fails

* **The build fails.** Fix the HIP build first. The later steps need a binary that builds.
:::

(rocgdb-bp-check-exists)=

## 2. Check that the breakpoint exists

By default, the HIP runtime loads GPU code objects only when the first kernel launches, so before the first launch, ROCgdb can't resolve a kernel name. ROCgdb asks whether to make the breakpoint pending. If you answer `n`, or run commands from a script, no breakpoint is created.

```shell
(gdb) break saxpy_kernel
(gdb) info breakpoints
```

ROCgdb prints:

```text
Function "saxpy_kernel" not defined.
Make breakpoint pending on future shared library load? (y or [n]) n
No breakpoints, watchpoints, tracepoints, or catchpoints.
```

Allow pending breakpoints, then set the breakpoint again:

```shell
(gdb) set breakpoint pending on
(gdb) break saxpy_kernel
```

ROCgdb prints:

```text
Function "saxpy_kernel" not defined.
Breakpoint 1 (saxpy_kernel) pending.
```

**Expected result:** `info breakpoints` lists the breakpoint with `<PENDING>` as its address until the runtime loads the GPU code objects.

:::{admonition} If this fails

* **`info breakpoints` still lists no breakpoint.** If you run commands from a script, put `set breakpoint pending on` before the `break` command.
:::

:::{tip}
If you set the breakpoint on a source line in GPU code, it can resolve to an unexpected place, often in host code in the same file, until the runtime loads the GPU code objects. Set it by kernel function name instead.
:::

(rocgdb-bp-check-launch)=

## 3. Confirm the application reaches the kernel launch

Set a breakpoint on the host line that launches the kernel, then run. In the `saxpy` example, find the launch line in `main.hip`:

```shell
$ grep -n saxpy_kernel main.hip
```

Use the line number of the launch, not the kernel definition. Host code is in the executable, so this breakpoint resolves as soon as you set it:

```shell
(gdb) break main.hip:<line-number>
(gdb) run
```

At the launch line, list the GPUs:

```shell
(gdb) info agents
```

**Expected result:** Execution stops at the launch line, and `info agents` lists every GPU you plan to debug with `A` (active) in the **State** column. ROCgdb printed no `amd-dbgapi` warnings.

The kernel breakpoint is still `<PENDING>` here, because the GPU code loads when the kernel launches. The launch statement spans two source lines, and `next` steps through them one at a time. In the example, the launch is lines 86 and 87, and the line numbers depend on the version of the example:

```text
86	  saxpy_kernel<<<dim3(grid_size), dim3(block_size), 0, hipStreamDefault>>>(
87	      a, d_x, d_y, size);
```

The launch doesn't run on the first `next`. In the example, three `next` commands move from line 86 to line 87, back to line 86, and then to line 90, and the launch runs on the third. Run `next` until ROCgdb moves past the launch, then check the kernel breakpoint:

```shell
(gdb) next
(gdb) info breakpoints
```

**Expected result:** ROCgdb stops in the kernel, or `info breakpoints` now shows an address for the kernel breakpoint instead of `<PENDING>`.

:::{admonition} If this fails

* **The kernel breakpoint still shows `<PENDING>` after the launch ran.** The kernel might be in a separate code object that loads later, for example through the module API `hipModuleLoad` or in a library. The breakpoint stays pending until that code object loads. Go to {ref}`step 4 <rocgdb-bp-check-deferred>`.
* **The program exits first.** Read its output. For example, when no GPU is visible to the application, it can print a HIP error such as `no ROCm-capable device is detected` and exit before it launches the kernel. Fix that problem in the application or the environment. It isn't a ROCgdb problem.
* **A GPU shows `U`, or no GPU is listed.** See {ref}`Check that ROCgdb can see your GPU <rocgdb-kl-check-gpu>`.
* **The output after `run` has a warning that mentions `amd-dbgapi` or `AMD GPU`.** Find the warning in {ref}`Read the startup warnings <rocgdb-kl-warnings>`.
:::

(rocgdb-bp-check-deferred)=

## 4. Check the kernel name and the code object

If the kernel breakpoint is still `<PENDING>` after the launch ran, there are two likely causes:

* **The name is wrong.** A misspelled name stays pending forever, and a mangled name works. After the runtime loads the code object, `info functions <name>` lists the GPU kernels, so you can check the spelling.
* **The kernel is in a separate code object that loads later**, for example through `hipModuleLoad` or in a library. The breakpoint stays pending until that code object loads. `HIP_ENABLE_DEFERRED_LOADING=0` doesn't change that.

If any kernel in the application has already run, the runtime has loaded the code object, so breakpoints on its other kernels resolve. This is true with or without `HIP_ENABLE_DEFERRED_LOADING=0`.

To make the kernel breakpoint resolve before the first kernel launches, ask the HIP runtime to load all GPU code objects at startup, then run the session again:

```shell
$ export HIP_ENABLE_DEFERRED_LOADING=0
$ rocgdb ./saxpy
```

In the new session, run `set breakpoint pending on` and set the breakpoint again, or run `break main`, `run`, and then `break saxpy_kernel`.

**Expected result:** All GPU code objects are loaded by the beginning of `main`, so the kernel breakpoint resolves before the kernel launches. When you stop at `main`, `info breakpoints` shows an address for the kernel breakpoint instead of `<PENDING>`.

:::{note}
Turning off deferred loading has limits. If the application calls `fork`, it might crash. If the application embeds many GPU code objects, ROCgdb might report errors because of open file limits.
:::

:::{admonition} If this fails

* **The breakpoint still isn't hit.** See the {ref}`breakpoint limitations <rocgdb-kl-breakpoints>` in {ref}`Known limitations <rocgdb-kl-limitations>`.
:::

## Interpret what you see

Find what you see in the first column.

```{list-table}
:header-rows: 1

* - What you see
  - What it means
  - What to do
  - Read more
* - The breakpoint is set but the source line is wrong or unavailable
  - The binary lacks debug information.
  - Rebuild with `-ggdb -O0` ({ref}`step 1 <rocgdb-bp-check-build>`).
  - {ref}`Compile with debug information <rocgdb-first-hip-kernel-build>`
* - `info breakpoints` reports no breakpoints after you set one, or the log shows `[answered N; input not from terminal]`
  - You answered `n` to the pending breakpoint prompt, or a script answered it for you.
  - Run `set breakpoint pending on`, then set the breakpoint again. In a script, put `set breakpoint pending on` at the top ({ref}`step 2 <rocgdb-bp-check-exists>`).
  - {ref}`Debug your first HIP kernel <rocgdb-first-hip-kernel>`
* - A source-line breakpoint stops in an unexpected place
  - The GPU code object that contains that line wasn't loaded when you set the breakpoint.
  - Set the breakpoint by function name ({ref}`step 2 <rocgdb-bp-check-exists>`).
  - [AMD GPU restrictions](https://rocm.docs.amd.com/projects/ROCgdb/en/latest/ROCgdb/gdb/doc/gdb/AMD-GPU.html#AMD-GPU-Restrictions)
* - The program exits before the host launch line
  - The kernel is never launched, for example because of a HIP runtime error.
  - Read the program's output and fix the error in the application or the environment ({ref}`step 3 <rocgdb-bp-check-launch>`).
  - {ref}`Check that ROCgdb can see your GPU <rocgdb-kl-check-gpu>`
* - A warning that mentions `amd-dbgapi` or `AMD GPU` after `run`, or `info agents` doesn't list your GPU as active
  - ROCgdb can't debug that GPU in this setup.
  - Check `info agents` and the warnings ({ref}`step 3 <rocgdb-bp-check-launch>`), then find the warning or the GPU in Known limitations.
  - {ref}`Read the startup warnings <rocgdb-kl-warnings>`, {ref}`Check that ROCgdb can see your GPU <rocgdb-kl-check-gpu>`
* - The breakpoint stays pending after the kernel should have run
  - The GPU code object that contains the kernel never loaded. This happens when the kernel is in a separate code object that's loaded later, such as through the module API or a library.
  - Check the kernel name, and check that the code object loads ({ref}`step 4 <rocgdb-bp-check-deferred>`). `HIP_ENABLE_DEFERRED_LOADING=0` only makes the breakpoint resolve before the first launch. It doesn't help when the code object itself loads later.
  - [AMD GPU restrictions](https://rocm.docs.amd.com/projects/ROCgdb/en/latest/ROCgdb/gdb/doc/gdb/AMD-GPU.html#AMD-GPU-Restrictions)
```

## Report a problem

If these steps don't resolve the problem, follow the routing and template in {ref}`Known limitations <rocgdb-kl-report>`. Report the problem to one of these places:

```{include} ../reference/known-limitations.md
:start-after: "% start-report-routing"
:end-before: "% end-report-routing"
```

:::{admonition} Evidence to collect

* The evidence from {ref}`Known limitations <rocgdb-kl-report>`: `rocgdb --version`, `rocminfo | grep gfx`, OS and kernel, and a session log.
* The compile command, including `-ggdb` and the `-O` level.
* The commands you ran and the output of `info breakpoints`.
* Whether the problem still happens with `HIP_ENABLE_DEFERRED_LOADING=0`.
:::

## You are done when

ROCgdb stops in your kernel at the breakpoint you set, and `info threads` shows the `AMDGPU Wave` that hit it. If it doesn't, you've found the known limitation that explains why, or opened an issue with the evidence.

## Related information

* {ref}`rocgdb-first-hip-kernel`
* {ref}`rocgdb-gpu-execution-state`
* {ref}`rocgdb-essential-commands`
