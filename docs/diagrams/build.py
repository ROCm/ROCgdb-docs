"""Render docs/diagrams/*.dot to docs/_static/rocgdb-<name>.svg with Graphviz,
and add an accessible title and description to each SVG.

Run from any directory: python3 -I docs/diagrams/build.py
"""
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE.parent / "_static"

ALT = {
    "known-limitations-checks": (
        "Checks for a ROCgdb problem",
        "Flowchart. Start: ROCgdb doesn't do what you expect. Check 1: does info agents list your GPU with state A? If no, step 2: read the amd-dbgapi warnings and fix the driver, firmware, runtime, or ROCm setup, then check again. If yes, check 3: is the GPU code built with -ggdb -O0 by a current ROCm compiler? If no, rebuild and check again. If yes, check 4: does a row in the limitations tables match? If yes, use the workaround in that row. If no, report a problem.",
    ),
    "known-limitations-report": (
        "Where to send a ROCgdb problem",
        "Flowchart. If the application doesn't work without ROCgdb, fix the application or ROCm setup first. If it works and a row in Known limitations matches, use that row's workaround, or accept the behavior as expected if the row has none. Otherwise, if the problem is in the documentation, open a ROCgdb-docs issue. If not, search ROCgdb issues, then open one with the evidence.",
    ),
    "wrong-results-steps": (
        "Steps to find a wrong value in a kernel",
        "Flowchart. Step 1: does catch hiperr stop on a HIP error? If yes, fix the failing HIP call. If no, step 2: work out which work-item wrote a wrong element. Step 3: stop only that work-item with a conditional breakpoint. Step 4: are the values it reads correct? If no, the bug is earlier, in a host copy or the kernel that produced the input. If yes, step 5: step and print. If the value goes wrong in this work-item, you found the line. If not, step 6: watch the output to see what overwrites it. That shows you the write that changes the value.",
    ),
    "wrong-results-report": (
        "Where to send a wrong-value problem",
        "Flowchart. Start: ROCgdb prints a value that differs from an independent one, such as a printf. If a row in Known limitations matches, use that row's workaround, or accept the behavior as expected if it has none. Otherwise, if the problem is in the documentation, open a ROCgdb-docs issue. If not, search ROCgdb issues, then open one with the evidence.",
    ),
    "attach-steps": (
        "Steps to attach ROCgdb to a running process",
        "Flowchart. If you can restart the application, restart it with HSA_ENABLE_DEBUG=1. If not, attach anyway, and waves that already exist might show a question mark in their IDs. Step 2: find the process ID. Step 3: does rocgdb -p PID attach? If not, fix ptrace permission or the container setup and try again, or start the application under ROCgdb instead. Step 4: does info threads show AMDGPU Wave entries? If yes, step 5a: inspect the waves that are running. If no, step 5b: break on the next kernel launch. Step 6: detach. The application keeps running.",
    ),
    "components": (
        "How ROCgdb fits together",
        "Block diagram. You use ROCgdb from the command line, the TUI, or an IDE through GDB/MI. ROCgdb works with your HIP application's host threads and memory, and with the AMD Debugger API library, ROCdbgapi. The ROCm compiler adds debug information to your application. The application runs on the HSA runtime (ROCr), which loads GPU code objects and lists them for ROCdbgapi. ROCgdb uses ROCdbgapi to read and control GPU state. ROCdbgapi uses the AMD Code Object Manager library, ROCcomgr, to disassemble GPU code, and the debug interface of the amdgpu driver's KFD interface to reach the AMD GPU, which has agents, queues, dispatches, waves, and lanes.",
    ),
}

# House style, shared by every diagram. The .dot files use these tokens so they
# hold only content and layout. Colors match the hand-drawn diagrams.
FONT = "Helvetica,Arial,sans-serif"
STYLE = {
    "@graph": f'graph [fontname="{FONT}", bgcolor="white", pad=0.15, nodesep=0.5, ranksep=0.4]',
    "@edge": f'edge [fontname="{FONT}", fontsize=12, color="#57606a", fontcolor="#57606a", arrowsize=0.8]',
    "@base": f'node [fontname="{FONT}", fontsize=13, fontcolor="#1f2328", margin="0.2,0.12", penwidth=1]',
    # Where the reader starts, and the GPU in the block diagram.
    "@dark": 'shape=box, style="rounded,filled", fillcolor="#3a4048", color="#1f2328", fontcolor="#ffffff"',
    # A question the reader answers. Square corners set it apart from actions.
    "@decision": 'shape=box, style=filled, fillcolor="#dbe8fb", color="#9db8e6", fontcolor="#0b57d0"',
    # Something the reader does, or a ROCgdb part in the block diagram.
    "@blue": 'shape=box, style="rounded,filled", fillcolor="#dbe8fb", color="#9db8e6", fontcolor="#0b57d0"',
    "@action": 'shape=box, style="rounded,filled", fillcolor="#f0f1f3", color="#c4cad0", fontcolor="#1f2328"',
    # Where a path ends.
    "@done": 'shape=box, style="rounded,filled", fillcolor="#ffffff", color="#0b57d0", penwidth=1.5, fontcolor="#1f2328"',
}


def expand(src):
    for token in sorted(STYLE, key=len, reverse=True):
        src = src.replace(token, STYLE[token])
    return src


for dot in sorted(HERE.glob("*.dot")):
    name = dot.stem
    svg = OUT / f"rocgdb-{name}.svg"
    subprocess.run(["dot", "-Tsvg", "-o", str(svg)], input=expand(dot.read_text()).encode(), check=True)
    title, desc = ALT[name]
    text = svg.read_text(encoding="utf-8")
    text = re.sub(r"<title>.*?</title>\s*", "", text, count=1, flags=re.S)
    text = text.replace(
        "<svg ",
        '<svg role="img" aria-labelledby="t d" ', 1,
    )
    text = re.sub(
        r"(<svg[^>]*>)",
        lambda m: f'{m.group(1)}\n<title id="t">{title}</title>\n<desc id="d">{desc}</desc>',
        text, count=1,
    )
    svg.write_text(text, encoding="utf-8")
    print("wrote", svg.name)
