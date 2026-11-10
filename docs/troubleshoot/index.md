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

* **The breakpoint is set but never stops.** Start with {ref}`rocgdb-bp-check-exists`, then work through the rest of {ref}`rocgdb-troubleshoot-breakpoint-not-hit`.
* **ROCgdb stops on a different line than the one you set.** Set the breakpoint by kernel function name ({ref}`rocgdb-bp-check-exists`), then disable deferred code loading ({ref}`rocgdb-bp-check-deferred`).
* **The program exits before the kernel runs.** Break on the host line that launches the kernel and read the program output ({ref}`rocgdb-bp-check-launch`).
* **Source lines are missing or wrong.** Rebuild with debug information ({ref}`rocgdb-bp-check-build`).

## All symptom pages

* {ref}`rocgdb-troubleshoot-breakpoint-not-hit`: You set a breakpoint in a HIP kernel and the application never stops there.

If your problem isn't listed, start with {ref}`rocgdb-gpu-execution-state` to confirm what state ROCgdb reports, then see {ref}`rocgdb-essential-commands`. If that doesn't help, [open an issue](https://github.com/ROCm/ROCgdb/issues).
