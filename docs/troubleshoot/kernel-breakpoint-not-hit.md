---
myst:
  html_meta:
    "description lang=en": "Troubleshoot a ROCgdb breakpoint in a HIP kernel that never stops. Check debug symbols, pending breakpoints, kernel launch, and deferred code loading."
    "keywords": "ROCgdb breakpoint not hit, kernel breakpoint, pending breakpoint, deferred loading, HIP_ENABLE_DEFERRED_LOADING"
---

% TODO(engineering validation): The original note said checks 2 and 3 were
% run against ROCgdb 16.3 (ROCm 7.2) on a system without a GPU. On such a
% system, only the "If this fails" branch of check 3 could be exercised
% (inferred from the page text, confirm with the author). Check 1 (build) has
% no recorded validation. Still to validate on a system with a supported GPU:
% the expected result of check 3 and all of check 4 (deferred loading). Add
% real sample output for each.

(rocgdb-troubleshoot-breakpoint-not-hit)=

# Kernel breakpoint isn't hit

Find out why ROCgdb doesn't stop at a breakpoint in a HIP kernel.

## When to use this page

Use this page when your application runs to completion, or runs past the point where you expect it to stop, and ROCgdb never stops in your GPU kernel. If you haven't stopped in a kernel before, start with {ref}`rocgdb-first-hip-kernel`.

## Prerequisites

* The application runs correctly without the debugger.
* You can reproduce the problem in a ROCgdb session.

## Steps

Work through these checks in order. Each one rules out a common cause.

(rocgdb-bp-check-build)=

### 1. Confirm the build has debug information

Rebuild the application with debug information (`-ggdb`) and no optimization (`-O0`), then start a new ROCgdb session. If you build with `hipcc`, use the same `-ggdb -O0` options.

```shell
$ amdclang++ -ggdb -O0 -x hip --offload-arch=native main.hip -o saxpy
```

:::{admonition} Expected result
:class: rocgdb-expected

The rebuilt binary runs without the debugger. If your build system already passes `-ggdb` and a low optimization level, you can skip the rebuild.
:::

(rocgdb-bp-check-exists)=

### 2. Check that the breakpoint exists

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

:::{admonition} Expected result
:class: rocgdb-expected

`info breakpoints` lists the breakpoint with `<PENDING>` as its address until the GPU code is loaded.
:::

:::{tip}
If you set the breakpoint on a source line in GPU code, it can resolve to an unexpected place before the GPU code is loaded. Set it by kernel function name instead.
:::

(rocgdb-bp-check-launch)=

### 3. Confirm the application reaches the kernel launch

Set a breakpoint on the host line that launches the kernel, then run. In the `saxpy` example, find the launch line in `main.hip`:

```shell
$ grep -n saxpy_kernel main.hip
```

Use the line number of the launch, not the kernel definition:

```shell
(gdb) break main.hip:<line-number>
(gdb) run
```

:::{admonition} Expected result
:class: rocgdb-expected

Execution stops at the launch line. Host code is loaded at startup, so this breakpoint resolves immediately.
:::

:::{admonition} If this fails
:class: rocgdb-iffails

If the program exits first, read its output. For example, when no GPU is visible to the application, it can print a HIP error such as `no ROCm-capable device is detected` and exit before it launches the kernel. Fix that problem in the application or the environment. It isn't a ROCgdb problem.
:::

(rocgdb-bp-check-deferred)=

### 4. Disable deferred code loading

If the application reaches the launch but the breakpoint stays pending, ask the HIP runtime to load all GPU code objects at startup, then run the session again.

```shell
$ export HIP_ENABLE_DEFERRED_LOADING=0
$ rocgdb ./saxpy
```

:::{admonition} Expected result
:class: rocgdb-expected

All GPU code objects are loaded by the beginning of `main`, so the kernel breakpoint resolves before the kernel launches.
:::

:::{note}
Disabling deferred loading has limits. If the application calls `fork`, it might crash. If the application embeds many device code objects, ROCgdb might report errors because of open file limits.
:::

## Interpret what you see

```{list-table}
:header-rows: 1
:widths: 40 60

* - What you see
  - Likely cause
* - `info breakpoints` reports no breakpoints after you set one
  - You answered `n` to the pending breakpoint prompt. Run `set breakpoint pending on` (check 2).
* - The program exits before the host launch line
  - The kernel is never launched, for example because of a HIP runtime error (check 3).
* - The breakpoint stays pending after the kernel should have run
  - The GPU code wasn't loaded. Disable deferred loading (check 4).
* - A source-line breakpoint stops in an unexpected place
  - The GPU code that contains that line wasn't loaded when you set the breakpoint. Set the breakpoint by function name (check 2).
* - The breakpoint is set but the source line is wrong or unavailable
  - The binary lacks debug information. Rebuild with `-ggdb -O0` (check 1).
```

## Report a problem

If these checks don't resolve the problem, [open an issue](https://github.com/ROCm/ROCgdb/issues) and include the following.

:::{admonition} Evidence to collect
:class: rocgdb-evidence

* The output of `show configuration`, which shows the ROCgdb build you're running.
* The ROCm version, GPU architecture, and operating system.
* The compile command, including optimization and debug flags.
* The commands you ran and the output of `info breakpoints`.
* Whether the problem still occurs with `HIP_ENABLE_DEFERRED_LOADING=0`.
:::

## Related information

* {ref}`rocgdb-first-hip-kernel`
* {ref}`rocgdb-gpu-execution-state`
* {ref}`rocgdb-essential-commands`
