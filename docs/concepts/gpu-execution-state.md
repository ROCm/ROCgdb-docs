---
myst:
  html_meta:
    "description lang=en": "Learn how ROCgdb represents GPU execution state: agents, queues, dispatches, waves as threads, and lanes as work-items, and which command shows each one."
    "keywords": "ROCgdb wave, ROCgdb lane, GPU threads, agents, queues, dispatches, AMDGPU wave"
---

(rocgdb-gpu-execution-state)=

# GPU execution state in ROCgdb

ROCgdb extends GDB's model of threads and frames to cover the GPU. This page maps each GPU concept to the ROCgdb command that shows it, so you know which command to run when you're stopped in a kernel.

## Concept map

```{list-table}
:header-rows: 1
:widths: 20 45 35

* - Concept
  - Description
  - Command
* - Agent
  - An AMD GPU (or other HSA agent) in the system
  - `info agents`
* - Queue
  - An HSA queue that receives kernel dispatches
  - `info queues`
* - Dispatch
  - One kernel launch, including grid and workgroup size
  - `info dispatches`
* - Wave
  - A GPU wave, listed as a GDB thread named `AMDGPU Wave`
  - `info threads`, `thread <id>`
* - Lane
  - One work-item of a wave
  - `info lanes`, `lane <id>`
* - Registers
  - The registers of the current wave
  - `info registers`, `info all-registers`
* - Address spaces
  - GPU memory regions, such as `global`, `local`, `private_wave`, and `private_lane`
  - `x <space>#<address>`
```

For example, `x/4xw global#<address>` prints four words of global memory in hexadecimal. For the other address spaces, see {ref}`rocgdb-essential-commands`.

## Waves are threads

A wave is a group of lanes (work-items) that execute together on the GPU. ROCgdb lists each wave in `info threads` next to the host CPU threads, and you select one with `thread <id>`. After you select a wave, commands such as `info registers` and `backtrace` apply to that wave.

The wave identifier in the `Target Id` column encodes where the wave sits in the system. In `AMDGPU Wave 1:2:1:1 (0,0,0)/0`, `1:2:1:1` gives the agent, queue, dispatch, and wave numbers, `(0,0,0)` gives the workgroup coordinates, and `/0` gives the wave's index within the workgroup.

## Lanes are work-items

A wave runs its lanes in lockstep. When you want to look at the values for one work-item, select a lane with `lane <id>`. Variable values you print after that belong to the selected lane. Use `info lanes` to list the lanes of the current wave and their state.

## Related information

```{eval-rst}
* To use these commands in a session, see :ref:`rocgdb-first-hip-kernel`.
* For the command syntax and more sample output, see :ref:`rocgdb-essential-commands`.
* For the complete model, see `Debugging on AMD GPU <../ROCgdb/gdb/doc/gdb/AMD-GPU.html>`_ in the ROCgdb user guide.
```
