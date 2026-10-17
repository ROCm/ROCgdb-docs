---
myst:
  html_meta:
    "description lang=en": "Pick what you see when a HIP application doesn't behave as expected in ROCgdb, such as a missed breakpoint, and get the checks that match your symptom."
    "keywords": "ROCgdb troubleshooting, debugging problems, kernel breakpoint, HIP debugging"
---

(rocgdb-troubleshoot)=

# Troubleshoot ROCgdb sessions

Select what you see to get the checks that match your symptom.

## Kernel breakpoint problems

```{eval-rst}
.. selector:: What do you see?
   :key: s

   .. selector-option:: Never stops
      :value: never-stops
      :default:
      :width: 4

   .. selector-option:: Stops in the wrong place
      :value: wrong-place
      :width: 4

   .. selector-option:: Exits early
      :value: exits-early
      :width: 4

.. selected:: s=never-stops

   You set a breakpoint in a HIP kernel and the application runs to completion without stopping there.

   1. Run ``info breakpoints``. If no breakpoint is listed, run ``set breakpoint pending on`` and set the breakpoint again. See :ref:`rocgdb-bp-check-exists`.
   2. Set a breakpoint on the host line that launches the kernel. If the program exits before that line, the kernel never launches. See :ref:`rocgdb-bp-check-launch`.
   3. If the breakpoint stays pending after the launch, set ``HIP_ENABLE_DEFERRED_LOADING=0`` and run the session again. See :ref:`rocgdb-bp-check-deferred`.

.. selected:: s=wrong-place

   You set a breakpoint on a source line in GPU code and ROCgdb stops somewhere else.

   1. Set the breakpoint by kernel function name instead of by source line. See :ref:`rocgdb-bp-check-exists`.
   2. Set ``HIP_ENABLE_DEFERRED_LOADING=0`` so the GPU code is loaded before you set the breakpoint. See :ref:`rocgdb-bp-check-deferred`.
   3. Rebuild with ``-ggdb -O0`` so line information is accurate. See :ref:`rocgdb-bp-check-build`.

.. selected:: s=exits-early

   The application ends before it reaches your kernel.

   1. Read the program output. A HIP error such as ``no ROCm-capable device is detected`` means the application exits before it launches the kernel. See :ref:`rocgdb-bp-check-launch`.
   2. Confirm the application runs correctly without the debugger. See the prerequisites in :ref:`rocgdb-troubleshoot-breakpoint-not-hit`.
```

For the full ordered checklist and the evidence to collect before you escalate, see {ref}`rocgdb-troubleshoot-breakpoint-not-hit`.

## All symptom pages

| What you see | Go to |
| --- | --- |
| You set a breakpoint in a HIP kernel and the application never stops there | {ref}`rocgdb-troubleshoot-breakpoint-not-hit` |

If your problem isn't listed, start with {ref}`rocgdb-gpu-execution-state` to confirm what state ROCgdb reports, then see {ref}`rocgdb-essential-commands`.
