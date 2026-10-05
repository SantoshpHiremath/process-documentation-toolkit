"""
Renders a process's steps as a real flowchart image via Graphviz --
the "editorial work and graphical representation of the processes"
task. Not a claim of experience with a
specific enterprise process-modeling tool (e.g. Signavio, ARIS,
Visio) -- this uses open-source Graphviz to produce an actual,
inspectable diagram from the structured process data, honestly
disclosed as that rather than BPMN-tool-specific experience.
"""

from __future__ import annotations

import graphviz

from src.process_model import ProcessStep

_SHAPE_BY_TYPE = {
    "start": "ellipse",
    "end": "ellipse",
    "task": "box",
    "decision": "diamond",
}

_COLOR_BY_TYPE = {
    "start": "#2E7D32",
    "end": "#2E7D32",
    "task": "#1B3A6B",
    "decision": "#B8860B",
}


def build_flowchart(steps: list[ProcessStep], process_id: str, process_name: str) -> graphviz.Digraph:
    """Builds a Graphviz Digraph for one process's steps. Raises
    ValueError if no steps match process_id, so a typo'd process_id
    fails loudly instead of silently producing an empty diagram."""
    process_steps = [s for s in steps if s.process_id == process_id]
    if not process_steps:
        raise ValueError(f"No steps found for process_id {process_id!r}")

    dot = graphviz.Digraph(name=process_id, comment=process_name)
    dot.attr(rankdir="TB", label=process_name, fontsize="16", labelloc="t")

    for step in process_steps:
        dot.node(
            step.step_id,
            label=f"{step.name}\\n({step.owner_role})",
            shape=_SHAPE_BY_TYPE[step.step_type],
            style="filled",
            fillcolor="white",
            color=_COLOR_BY_TYPE[step.step_type],
            fontcolor=_COLOR_BY_TYPE[step.step_type],
        )

    for step in process_steps:
        for branch_label, target_id in step.next_steps.items():
            dot.edge(step.step_id, target_id, label=branch_label if branch_label else None)

    return dot


def render_flowchart_png(steps: list[ProcessStep], process_id: str, process_name: str, output_path: str) -> str:
    """Renders the flowchart to a real PNG file on disk and returns the
    path actually written. Graphviz's render() appends the format
    extension itself, so the returned path may differ slightly from a
    naively-constructed one -- returning what render() actually
    reports keeps this honest rather than assuming a filename."""
    dot = build_flowchart(steps, process_id, process_name)
    rendered_path = dot.render(filename=output_path, format="png", cleanup=True)
    return rendered_path
