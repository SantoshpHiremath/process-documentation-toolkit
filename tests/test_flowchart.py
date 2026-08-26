import os

import pytest

from src.flowchart import build_flowchart, render_flowchart_png
from src.process_model import PROCESS_STEPS, ProcessStep


def test_build_flowchart_includes_all_nodes_for_process():
    dot = build_flowchart(PROCESS_STEPS, "PR01", "Supplier Onboarding")
    source = dot.source
    for step in [s for s in PROCESS_STEPS if s.process_id == "PR01"]:
        assert step.step_id in source


def test_build_flowchart_raises_for_unknown_process_id():
    with pytest.raises(ValueError):
        build_flowchart(PROCESS_STEPS, "NOT_A_REAL_PROCESS", "Nonexistent")


def test_build_flowchart_includes_decision_branch_labels():
    dot = build_flowchart(PROCESS_STEPS, "PR01", "Supplier Onboarding")
    source = dot.source
    assert "yes" in source
    assert "no" in source


def test_render_flowchart_png_writes_a_real_file(tmp_path):
    output_path = str(tmp_path / "test_flowchart")
    written_path = render_flowchart_png(PROCESS_STEPS, "PR02", "Expense Approval", output_path)
    assert os.path.exists(written_path)
    assert written_path.endswith(".png")
    # A real rendered PNG should be nontrivially sized -- catches a
    # silently-empty or corrupt render, not just "a file exists".
    assert os.path.getsize(written_path) > 1000


def test_step_type_validation_rejects_unknown_type():
    with pytest.raises(ValueError):
        ProcessStep("X", "P1", "not_a_real_type", "name", "role", {})
