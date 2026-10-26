---
myst:
  html_meta:
    "description lang=en": "Pick what you see when a HIP application doesn't behave as expected in ROCgdb, such as a missed breakpoint, and get the checks that match your symptom."
    "keywords": "ROCgdb troubleshooting, debugging problems, kernel breakpoint, HIP debugging"
---

(rocgdb-troubleshoot)=

# Troubleshoot ROCgdb problems

Find the checks that match what you see.

```{raw} html
<noscript><p><strong>JavaScript is turned off.</strong> The symptom selector needs it. Use the full checklist instead: <a href="kernel-breakpoint-not-hit.html">Kernel breakpoint isn't hit</a>.</p></noscript>
```

## Kernel breakpoint problems

% The checklist page (kernel-breakpoint-not-hit.md) is canonical. Keep each
% selector branch to one sentence and a link so the two don't drift apart.
% The selector needs JavaScript, so print builds use the plain list below it.

```{eval-rst}
.. only:: html

   .. selector:: What do you see?
      :key: s

      .. selector-option:: The breakpoint is set but never stops
         :value: never-stops
         :default:
         :width: 4

      .. selector-option:: It stops on a different line than I set
         :value: wrong-place
         :width: 4

      .. selector-option:: The program exits before the kernel runs
         :value: exits-early
         :width: 4

   .. selected:: s=never-stops

      The application runs to completion without stopping at your breakpoint. Start with :ref:`rocgdb-bp-check-exists`, then check :ref:`rocgdb-bp-check-launch` and :ref:`rocgdb-bp-check-deferred`.

   .. selected:: s=wrong-place

      ROCgdb stops somewhere other than the line you set. Start with :ref:`rocgdb-bp-check-exists`, then check :ref:`rocgdb-bp-check-deferred` and :ref:`rocgdb-bp-check-build`.

   .. selected:: s=exits-early

      The application ends before it reaches your kernel. Start with :ref:`rocgdb-bp-check-launch`, then confirm the prerequisites in :ref:`rocgdb-troubleshoot-breakpoint-not-hit`.

.. only:: not html

   * **The breakpoint is set but never stops:** the application runs to completion without stopping at your breakpoint. See :ref:`rocgdb-bp-check-exists`, :ref:`rocgdb-bp-check-launch`, and :ref:`rocgdb-bp-check-deferred`.
   * **It stops on a different line than I set:** ROCgdb stops somewhere other than the line you set. See :ref:`rocgdb-bp-check-exists`, :ref:`rocgdb-bp-check-deferred`, and :ref:`rocgdb-bp-check-build`.
   * **The program exits before the kernel runs:** the application ends before it reaches your kernel. See :ref:`rocgdb-bp-check-launch` and :ref:`rocgdb-troubleshoot-breakpoint-not-hit`.
```

For the full ordered checklist and the evidence to include in an issue, see {ref}`rocgdb-troubleshoot-breakpoint-not-hit`.

## All symptom pages

* {ref}`rocgdb-troubleshoot-breakpoint-not-hit`: You set a breakpoint in a HIP kernel and the application never stops there.

If your problem isn't listed, start with {ref}`rocgdb-gpu-execution-state` to confirm what state ROCgdb reports, then see {ref}`rocgdb-essential-commands`. If that doesn't help, [open an issue](https://github.com/ROCm/ROCgdb/issues).
