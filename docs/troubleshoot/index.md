---
myst:
  html_meta:
    "description lang=en": "Find the ROCgdb checks that match what you see in a HIP application: a kernel breakpoint that never stops, wrong output values, or a GPU that ROCgdb doesn't list."
    "keywords": "ROCgdb troubleshooting, debugging problems, kernel breakpoint, HIP debugging"
---

(rocgdb-troubleshoot)=

# Troubleshoot ROCgdb problems

Find the checks that match what you see.

## Kernel breakpoint problems

If a kernel breakpoint never stops, or stops somewhere you don't expect, start here.

% The checklist page (kernel-breakpoint-not-hit.md) is canonical. Each
% section below gives the short inline steps, drawn from that page, and
% links to the full check. If you change a command there, change it here.
% The never-stops section ends with the build check because missing debug
% information can also make a breakpoint appear to never stop.

### The breakpoint is set but never stops

The application runs to completion without stopping at your breakpoint.

1. Allow pending breakpoints, then set the breakpoint by kernel name: `set breakpoint pending on`, then `break saxpy_kernel`. See {ref}`Check that the breakpoint exists <rocgdb-bp-check-exists>`.
2. Set a breakpoint on the host line that launches the kernel, then `run`. If the program exits first, read its output. At the launch line, `info agents` lists every GPU you plan to debug with `A`, and the output after `run` has no warnings that mention `amd-dbgapi`. See {ref}`Confirm the application reaches the kernel launch <rocgdb-bp-check-launch>`.
3. Run `next` until the launch executes, then `info breakpoints`. The kernel breakpoint now shows an address. The launch statement can span two source lines, so it can take more than one `next` to run it. If the breakpoint still shows `<PENDING>` after the launch, check the kernel name. Also check whether the kernel is in a code object that loads later, for example through `hipModuleLoad` or a library. `HIP_ENABLE_DEFERRED_LOADING=0` doesn't help in that case. See {ref}`Check the kernel name and the code object <rocgdb-bp-check-deferred>`.
4. If the source lines are missing, or none of the preceding steps helps, rebuild with `-ggdb -O0` and start a new session. See {ref}`Confirm the build has debug information <rocgdb-bp-check-build>`.
5. If the breakpoint still doesn't stop, check the {ref}`known limitations <rocgdb-kl-limitations>`.

### The breakpoint stops on a different line than you set

ROCgdb stops somewhere other than the line you set.

1. Set the breakpoint by kernel function name instead of by source line, with `set breakpoint pending on` first. See {ref}`Check that the breakpoint exists <rocgdb-bp-check-exists>`.
2. If the source line is wrong or unavailable, rebuild with `-ggdb -O0` and start a new session. See {ref}`Confirm the build has debug information <rocgdb-bp-check-build>`.

### The program exits before the kernel runs

The application ends before it reaches your kernel.

1. Set a breakpoint on the host line that launches the kernel, then `run`. If the program exits first, read its output for a HIP error such as `no ROCm-capable device is detected`. See {ref}`Confirm the application reaches the kernel launch <rocgdb-bp-check-launch>`.
2. If the application runs correctly outside the debugger but exits under ROCgdb, check that ROCgdb can see your GPU and read any startup warnings that mention `amd-dbgapi` or `AMD GPU`. See {ref}`Check that ROCgdb can see your GPU <rocgdb-kl-check-gpu>` and {ref}`Read the startup warnings <rocgdb-kl-warnings>`.

For the full ordered steps and the evidence to include in an issue, see {ref}`rocgdb-troubleshoot-breakpoint-not-hit`.

## Wrong results

If the application runs but its output is wrong, start here.

% The wrong-results page is canonical. Each step below is a short form of a
% step there. If you change a command there, change it here.

### The kernel runs but some output values are wrong

The application runs to completion, but some output elements aren't what you expect, or a value you print in ROCgdb looks wrong.

1. Stop on any HIP API error with `catch hiperr`, then run. See {ref}`Rule out HIP API errors <rocgdb-wr-check-hiperr>`.
2. Work out which work-item wrote the wrong element, and stop only that work-item with a conditional breakpoint. See {ref}`Work out which work-item wrote the wrong element <rocgdb-wr-find-workitem>` and {ref}`Stop only that work-item <rocgdb-wr-stop-workitem>`.
3. Print the values that work-item reads. If an input is already wrong, the bug is earlier. See {ref}`Check the values this work-item reads <rocgdb-wr-check-inputs>`.
4. Step through and print the output element. See {ref}`Step through and print the value <rocgdb-wr-step-print>`.
5. If the value is right when the work-item writes it, watch the location to find what overwrites it. See {ref}`Find what overwrites the output <rocgdb-wr-watch>`.

For the full ordered steps and the evidence to include in an issue, see {ref}`rocgdb-troubleshoot-wrong-results`.

## GPU and setup problems

If ROCgdb can't debug your GPU, start here.

### ROCgdb doesn't list your GPU or prints an `amd-dbgapi` or `AMD GPU` warning

ROCgdb can't see your GPU, or it prints a warning about the driver, firmware, or runtime.

1. Run `info agents`, and check that every GPU you plan to debug appears with `A`. See {ref}`Check that ROCgdb can see your GPU <rocgdb-kl-check-gpu>`.
2. Scroll back to where you typed `run`, and look for a warning that mentions `amd-dbgapi` or `AMD GPU`. See {ref}`Read the startup warnings <rocgdb-kl-warnings>`.

## All troubleshooting pages

* {ref}`rocgdb-troubleshoot-breakpoint-not-hit`: Your kernel breakpoint never stops, stops on the wrong line, or the application exits before the kernel runs.
* {ref}`rocgdb-troubleshoot-wrong-results`: Your kernel runs to completion but some output values are wrong, or a value you print isn't what you expect.
* {ref}`rocgdb-known-limitations`: ROCgdb doesn't see your GPU, prints a warning that mentions `amd-dbgapi` or `AMD GPU`, or a feature doesn't work the way it does in CPU code.

If your problem isn't listed, check whether it's a {ref}`known limitation <rocgdb-kl-limitations>`. If no row matches, follow {ref}`Report a problem <rocgdb-kl-report>` to choose where to send it and what evidence to include.
