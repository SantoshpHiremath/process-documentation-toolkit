"""
Change-request workflow logic: filtering by status, summarizing
open/pending work per process -- the posting's "you take over requests
for documentation and implementation in the tool" task, modeled as a
real, queryable workflow rather than an unordered list.
"""

from __future__ import annotations

from src.process_model import ChangeRequest

_OPEN_STATUSES = {"submitted", "in_review"}


def open_requests(requests: list[ChangeRequest]) -> list[ChangeRequest]:
    return [r for r in requests if r.status in _OPEN_STATUSES]


def requests_for_process(requests: list[ChangeRequest], process_id: str) -> list[ChangeRequest]:
    return [r for r in requests if r.process_id == process_id]


def summarize_by_status(requests: list[ChangeRequest]) -> dict[str, int]:
    summary: dict[str, int] = {}
    for r in requests:
        summary[r.status] = summary.get(r.status, 0) + 1
    return summary


def oldest_open_request(requests: list[ChangeRequest]) -> ChangeRequest | None:
    """The longest-waiting open request -- useful for a process
    coordinator triaging what to pick up next. Returns None if there
    are no open requests."""
    open_ones = open_requests(requests)
    if not open_ones:
        return None
    return min(open_ones, key=lambda r: r.submitted_date)
