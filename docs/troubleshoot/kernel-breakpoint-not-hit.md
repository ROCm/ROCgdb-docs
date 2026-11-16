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

Use this page when your application runs to completion, or runs past the point where you expect it to stop, and ROCgdb never stops in your GPU kernel. If you haven't stopped in a kernel before, start with {ref}`rocgdb-first-hip-kernel`.

Work through the steps in order. Each one rules out a common cause.

## Prerequisites

* The application runs correctly without the debugger.
* You can reproduce the problem in a ROCgdb session.

(rocgdb-bp-check-build)=

## 1. Confirm the build has debug information

If your build already uses `-ggdb -O0`, skip to {ref}`step 2 <rocgdb-bp-check-exists>`. Otherwise, rebuild the application with debug information (`-ggdb`) and no optimization (`-O0`), then start a new ROCgdb session. If you build with `hipcc`, use the same `-ggdb -O0` options.

```shell
$ amdclang++ -ggdb -O0 -x hip --offload-arch=native -I../../Common main.hip -o saxpy
```

**Expected result:** The rebuilt binary runs without the debugger.

(rocgdb-bp-check-exists)=

## 2. Check that the breakpoint exists

By default, the HIP runtime loads GPU code only when the first kernel launches, so ROCgdb can't resolve a kernel name when you set the breakpoint. ROCgdb asks whether to make the breakpoint pending. If you answer `n`, or run commands from a script, no breakpoint is created.

```shell
(gdb) break saxpy_kernel
Function "saxpy_kernel" not defined.
Make breakpoint pending on future shared library load? (y or [n]) n
(gdb) info breakpoints
No breakpoints, watchpoints, tracepoints, or catchpoints.
```

Allow pending breakpoints, then set the breakpoint again:

```shell
(gdb) set breakpoint pending on
(gdb) break saxpy_kernel
Function "saxpy_kernel" not defined.
Breakpoint 1 (saxpy_kernel) pending.
```

**Expected result:** `info breakpoints` lists the breakpoint with `<PENDING>` as its address until the GPU code is loaded.

:::{tip}
If you set the breakpoint on a source line in GPU code, it can resolve to an unexpected place before the GPU code is loaded. Set it by kernel function name instead.
:::

(rocgdb-bp-check-launch)=

## 3. Confirm the application reaches the kernel launch

Set a breakpoint on the host line that launches the kernel, then run. In the `saxpy` example, find the launch line in `main.hip`:

```shell
$ grep -n saxpy_kernel main.hip
```

Use the line number of the launch, not the kernel definition:

```shell
(gdb) break main.hip:<line-number>
(gdb) run
```

At the launch line, list the GPUs:

```shell
(gdb) info agents
```

**Expected result:** Execution stops at the launch line. Host code is loaded at startup, so this breakpoint resolves immediately. `info agents` lists every GPU you plan to debug with `A` (active) in the **State** column, and ROCgdb printed no `amd-dbgapi` warnings when it started.

:::{admonition} If this fails

* **The program exits first.** Read its output. For example, when no GPU is visible to the application, it can print a HIP error such as `no ROCm-capable device is detected` and exit before it launches the kernel. Fix that problem in the application or the environment. It isn't a ROCgdb problem.
* **A GPU shows `U`, or no GPU is listed.** See {ref}`Check that ROCgdb can see your GPU <rocgdb-kl-check-gpu>`.
* **ROCgdb printed an `amd-dbgapi` warning.** Find the warning in {ref}`Read the startup warnings <rocgdb-kl-warnings>`.
:::

(rocgdb-bp-check-deferred)=

## 4. Turn off deferred code loading

If the application reaches the launch but the breakpoint stays pending, ask the HIP runtime to load all GPU code objects at startup, then run the session again.

```shell
$ export HIP_ENABLE_DEFERRED_LOADING=0
$ rocgdb ./saxpy
```

**Expected result:** All GPU code objects are loaded by the beginning of `main`, so the kernel breakpoint resolves before the kernel launches.

:::{note}
Turning off deferred loading has limits. If the application calls `fork`, it might crash. If the application embeds many device code objects, ROCgdb might report errors because of open file limits.
:::

If the breakpoint still doesn't stop after these steps, check whether what you're doing is a {ref}`known limitation <rocgdb-kl-limitations>`.

## Interpret what you see

Find what you see in the first column.

```{list-table}
:header-rows: 1

* - What you see
  - What it means
  - What to do
  - Read more
* - `info breakpoints` reports no breakpoints after you set one
  - You answered `n` to the pending breakpoint prompt, or a script answered it for you.
  - Run `set breakpoint pending on`, then set the breakpoint again.
  - {ref}`Step 2 <rocgdb-bp-check-exists>`
* - The program exits before the host launch line
  - The kernel is never launched, for example because of a HIP runtime error.
  - Read the program's output and fix the error in the application or the environment.
  - {ref}`Step 3 <rocgdb-bp-check-launch>`
* - The breakpoint stays pending after the kernel should have run
  - The GPU code wasn't loaded.
  - Turn off deferred loading with `HIP_ENABLE_DEFERRED_LOADING=0`.
  - {ref}`Step 4 <rocgdb-bp-check-deferred>`
* - A source-line breakpoint stops in an unexpected place
  - The GPU code that contains that line wasn't loaded when you set the breakpoint.
  - Set the breakpoint by function name.
  - {ref}`Step 2 <rocgdb-bp-check-exists>`
* - The breakpoint is set but the source line is wrong or unavailable
  - The binary lacks debug information.
  - Rebuild with `-ggdb -O0`.
  - {ref}`Step 1 <rocgdb-bp-check-build>`
* - An `amd-dbgapi` warning at startup, or `info agents` doesn't list your GPU as active
  - ROCgdb can't debug that GPU in this setup.
  - Find the warning or the GPU in Known limitations.
  - {ref}`Step 3 <rocgdb-bp-check-launch>`
```

## Report a problem

If these steps don't resolve the problem, follow the routing and template in {ref}`Known limitations <rocgdb-kl-report>`.

:::{admonition} Evidence to collect

* The evidence from {ref}`Known limitations <rocgdb-kl-report>`: `rocgdb --version`, `rocminfo | grep gfx`, OS and kernel, and a session log.
* The compile command, including `-ggdb` and the `-O` level.
* The commands you ran and the output of `info breakpoints`.
* Whether the problem still happens with `HIP_ENABLE_DEFERRED_LOADING=0`.
:::

Open the issue on [ROCm/ROCgdb issues](https://github.com/ROCm/ROCgdb/issues).

## You are done when

ROCgdb stops in your kernel at the breakpoint you set, and `info threads` shows the `AMDGPU Wave` that hit it.

## Related information

* {ref}`rocgdb-first-hip-kernel`
* {ref}`rocgdb-gpu-execution-state`
* {ref}`rocgdb-essential-commands`
