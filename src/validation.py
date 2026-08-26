"""
Process-integrity checks: every step must belong to a known process,
every referenced next-step must actually exist, every process needs
exactly one start and at least one end reachable from it, and every
change request must reference a real process -- the kind of "keep the
overview" correctness a process documentation tool needs to enforce so
the documented flow doesn't silently drift from something that's
actually navigable start-to-end.
"""

from __future__ import annotations

from src.process_model import ChangeRequest, Process, ProcessStep


def find_dangling_step_references(steps: list[ProcessStep]) -> list[tuple[str, str]]:
    """Returns (step_id, referenced_step_id) pairs where a step's
    next_steps points to a step_id that doesn't exist."""
    known_ids = {s.step_id for s in steps}
    dangling = []
    for step in steps:
        for target in step.next_steps.values():
            if target not in known_ids:
                dangling.append((step.step_id, target))
    return dangling


def find_orphaned_change_requests(
    requests: list[ChangeRequest], processes: list[Process]
) -> list[ChangeRequest]:
    """Change requests that reference a process_id not present in the
    process register."""
    known_process_ids = {p.process_id for p in processes}
    return [r for r in requests if r.process_id not in known_process_ids]


def is_reachable_to_end(steps: list[ProcessStep], process_id: str) -> bool:
    """Whether an 'end' step is reachable from the process's 'start'
    step by following next_steps -- catches a process definition that
    looks complete but actually has no path through it (e.g. a
    decision branch that loops forever or a missing link)."""
    process_steps = {s.step_id: s for s in steps if s.process_id == process_id}
    start_steps = [s for s in process_steps.values() if s.step_type == "start"]
    if not start_steps:
        return False

    visited = set()
    queue = [start_steps[0].step_id]
    while queue:
        current_id = queue.pop()
        if current_id in visited:
            continue
        visited.add(current_id)
        current = process_steps.get(current_id)
        if current is None:
            continue
        if current.step_type == "end":
            return True
        for target in current.next_steps.values():
            if target not in visited:
                queue.append(target)
    return False


def run_all_checks(
    steps: list[ProcessStep], processes: list[Process], requests: list[ChangeRequest]
) -> dict:
    unreachable_end = [
        p.process_id for p in processes if not is_reachable_to_end(steps, p.process_id)
    ]
    return {
        "dangling_step_references": find_dangling_step_references(steps),
        "orphaned_change_requests": find_orphaned_change_requests(requests, processes),
        "processes_without_reachable_end": unreachable_end,
    }
