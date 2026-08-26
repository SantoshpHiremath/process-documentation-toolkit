from datetime import date

from src.change_requests import (
    oldest_open_request,
    open_requests,
    requests_for_process,
    summarize_by_status,
)
from src.process_model import ChangeRequest


def test_open_requests_excludes_implemented_and_rejected():
    requests = [
        ChangeRequest("A", "P1", "r", "d", "submitted", date(2026, 1, 1)),
        ChangeRequest("B", "P1", "r", "d", "in_review", date(2026, 1, 1)),
        ChangeRequest("C", "P1", "r", "d", "implemented", date(2026, 1, 1)),
        ChangeRequest("D", "P1", "r", "d", "rejected", date(2026, 1, 1)),
    ]
    result = open_requests(requests)
    assert {r.request_id for r in result} == {"A", "B"}


def test_requests_for_process_filters_correctly():
    requests = [
        ChangeRequest("A", "P1", "r", "d", "submitted", date(2026, 1, 1)),
        ChangeRequest("B", "P2", "r", "d", "submitted", date(2026, 1, 1)),
    ]
    result = requests_for_process(requests, "P1")
    assert [r.request_id for r in result] == ["A"]


def test_summarize_by_status_counts_correctly():
    requests = [
        ChangeRequest("A", "P1", "r", "d", "submitted", date(2026, 1, 1)),
        ChangeRequest("B", "P1", "r", "d", "submitted", date(2026, 1, 1)),
        ChangeRequest("C", "P1", "r", "d", "implemented", date(2026, 1, 1)),
    ]
    result = summarize_by_status(requests)
    assert result == {"submitted": 2, "implemented": 1}


def test_oldest_open_request_returns_earliest_by_date():
    requests = [
        ChangeRequest("A", "P1", "r", "d", "submitted", date(2026, 3, 1)),
        ChangeRequest("B", "P1", "r", "d", "submitted", date(2026, 1, 1)),
        ChangeRequest("C", "P1", "r", "d", "submitted", date(2026, 2, 1)),
    ]
    result = oldest_open_request(requests)
    assert result.request_id == "B"


def test_oldest_open_request_ignores_closed_requests():
    requests = [
        ChangeRequest("A", "P1", "r", "d", "implemented", date(2026, 1, 1)),
    ]
    assert oldest_open_request(requests) is None


def test_oldest_open_request_returns_none_for_empty_list():
    assert oldest_open_request([]) is None
