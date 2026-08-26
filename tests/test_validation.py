from datetime import date

from src.process_model import ChangeRequest, Process, ProcessStep
from src.validation import (
    find_dangling_step_references,
    find_orphaned_change_requests,
    is_reachable_to_end,
    run_all_checks,
)


def test_find_dangling_step_references_none_in_valid_flow():
    steps = [
        ProcessStep("A", "P1", "start", "start", "role", {"": "B"}),
        ProcessStep("B", "P1", "end", "end", "role", {}),
    ]
    assert find_dangling_step_references(steps) == []


def test_find_dangling_step_references_catches_missing_target():
    steps = [
        ProcessStep("A", "P1", "start", "start", "role", {"": "MISSING"}),
    ]
    result = find_dangling_step_references(steps)
    assert result == [("A", "MISSING")]


def test_find_dangling_step_references_checks_all_decision_branches():
    steps = [
        ProcessStep("A", "P1", "decision", "decide", "role", {"yes": "B", "no": "MISSING"}),
        ProcessStep("B", "P1", "end", "end", "role", {}),
    ]
    result = find_dangling_step_references(steps)
    assert result == [("A", "MISSING")]


def test_find_orphaned_change_requests_catches_unknown_process():
    processes = [Process("P1", "Real Process", "owner", "1.0", date(2026, 1, 1))]
    requests = [
        ChangeRequest("CR1", "P1", "requester", "desc", "submitted", date(2026, 1, 1)),
        ChangeRequest("CR2", "P99", "requester", "desc", "submitted", date(2026, 1, 1)),
    ]
    result = find_orphaned_change_requests(requests, processes)
    assert [r.request_id for r in result] == ["CR2"]


def test_is_reachable_to_end_true_for_simple_linear_flow():
    steps = [
        ProcessStep("A", "P1", "start", "start", "role", {"": "B"}),
        ProcessStep("B", "P1", "task", "task", "role", {"": "C"}),
        ProcessStep("C", "P1", "end", "end", "role", {}),
    ]
    assert is_reachable_to_end(steps, "P1") is True


def test_is_reachable_to_end_true_through_decision_branch():
    steps = [
        ProcessStep("A", "P1", "start", "start", "role", {"": "B"}),
        ProcessStep("B", "P1", "decision", "decide", "role", {"yes": "C", "no": "A"}),
        ProcessStep("C", "P1", "end", "end", "role", {}),
    ]
    assert is_reachable_to_end(steps, "P1") is True


def test_is_reachable_to_end_false_when_no_end_reachable():
    # A loops back to B forever, no end step ever reached.
    steps = [
        ProcessStep("A", "P1", "start", "start", "role", {"": "B"}),
        ProcessStep("B", "P1", "task", "task", "role", {"": "A"}),
    ]
    assert is_reachable_to_end(steps, "P1") is False


def test_is_reachable_to_end_false_when_no_start_step():
    steps = [
        ProcessStep("A", "P1", "task", "task", "role", {"": "B"}),
        ProcessStep("B", "P1", "end", "end", "role", {}),
    ]
    assert is_reachable_to_end(steps, "P1") is False


def test_run_all_checks_on_real_portfolio_data_is_clean():
    from src.process_model import CHANGE_REQUESTS, PROCESS_STEPS, PROCESSES
    result = run_all_checks(PROCESS_STEPS, PROCESSES, CHANGE_REQUESTS)
    assert result["dangling_step_references"] == []
    assert result["processes_without_reachable_end"] == []


def test_run_all_checks_catches_the_deliberate_orphaned_request():
    from src.process_model import CHANGE_REQUESTS, PROCESS_STEPS, PROCESSES
    result = run_all_checks(PROCESS_STEPS, PROCESSES, CHANGE_REQUESTS)
    orphaned_ids = [r.request_id for r in result["orphaned_change_requests"]]
    assert "CR04" in orphaned_ids
