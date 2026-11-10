---
myst:
  html_meta:
    "description lang=en": "Find the checks that match what you see when a HIP application doesn't behave as expected in ROCgdb, such as a missed breakpoint."
    "keywords": "ROCgdb troubleshooting, debugging problems, kernel breakpoint, HIP debugging"
---

(rocgdb-troubleshoot)=

# Troubleshoot ROCgdb problems

Find the checks that match what you see.

## Kernel breakpoint problems

% The checklist page (kernel-breakpoint-not-hit.md) is canonical. Each
% section below gives the short inline steps, drawn from that page, and
% links to the full check. If you change a command there, change it here.
% The never-stops section ends with the build check because missing debug
% information can also make a breakpoint appear to never stop.

### The breakpoint is set but never stops

The application runs to completion without stopping at your breakpoint.

1. Allow pending breakpoints, then set the breakpoint by kernel name: `set breakpoint pending on`, then `break saxpy_kernel`. See {ref}`rocgdb-bp-check-exists`.
2. Set a breakpoint on the host line that launches the kernel, then `run`. If the program exits first, read its output. See {ref}`rocgdb-bp-check-launch`.
3. If the launch is reached but the breakpoint stays `<PENDING>`, run `export HIP_ENABLE_DEFERRED_LOADING=0` and start a new session. See {ref}`rocgdb-bp-check-deferred`.
4. If the source lines are missing, or none of the above helps, rebuild with `-ggdb -O0` and start a new session. See {ref}`rocgdb-bp-check-build`.

### It stops on a different line than I set

ROCgdb stops somewhere other than the line you set.

1. Set the breakpoint by kernel function name instead of by source line, with `set breakpoint pending on` first. See {ref}`rocgdb-bp-check-exists`.
2. Run `export HIP_ENABLE_DEFERRED_LOADING=0` so that the GPU code is loaded before you set the breakpoint. See {ref}`rocgdb-bp-check-deferred`.
3. If the source line is wrong or unavailable, rebuild with `-ggdb -O0` and start a new session. See {ref}`rocgdb-bp-check-build`.

### The program exits before the kernel runs

The application ends before it reaches your kernel.

1. Set a breakpoint on the host line that launches the kernel, then `run`. If the program exits first, read its output for a HIP error such as `no ROCm-capable device is detected`. See {ref}`rocgdb-bp-check-launch`.
2. If the application runs correctly outside the debugger, work through the full checklist in {ref}`rocgdb-troubleshoot-breakpoint-not-hit`.

For the full ordered checklist and the evidence to include in an issue, see {ref}`rocgdb-troubleshoot-breakpoint-not-hit`.

## All symptom pages

* {ref}`rocgdb-troubleshoot-breakpoint-not-hit`: You set a breakpoint in a HIP kernel and the application never stops there.

If your problem isn't listed, start with {ref}`rocgdb-gpu-execution-state` to confirm what state ROCgdb reports, then see {ref}`rocgdb-essential-commands`. If that doesn't help, [open an issue](https://github.com/ROCm/ROCgdb/issues).
