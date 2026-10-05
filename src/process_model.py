"""
A structured business-process register: processes made of typed steps
(task, decision, start, end) with owners and a defined flow, plus
change requests for documentation updates -- the underlying data model
that documenting business processes in a structured tool and handling
requests for documentation and implementation need,
built and stored as real, inspectable, testable structures rather than
free-text descriptions.

All process content below is invented, modeled loosely on a fictional
company's supplier-onboarding and expense-approval processes -- not
real process data from any company.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

STEP_TYPES = {"start", "task", "decision", "end"}


@dataclass(frozen=True)
class ProcessStep:
    step_id: str
    process_id: str
    step_type: str  # one of STEP_TYPES
    name: str
    owner_role: str
    # next_steps: for a "decision" step, a dict of {branch_label: step_id};
    # for any other step type, a dict with a single entry {"": step_id},
    # or empty for an "end" step.
    next_steps: dict = field(default_factory=dict)

    def __post_init__(self):
        if self.step_type not in STEP_TYPES:
            raise ValueError(f"Unknown step_type {self.step_type!r}, must be one of {STEP_TYPES}")


@dataclass(frozen=True)
class Process:
    process_id: str
    name: str
    process_owner: str
    version: str
    last_updated: date


@dataclass(frozen=True)
class ChangeRequest:
    request_id: str
    process_id: str
    requested_by: str
    description: str
    status: str  # "submitted", "in_review", "implemented", "rejected"
    submitted_date: date


PROCESSES: list[Process] = [
    Process("PR01", "Supplier Onboarding", "J. Reyes (Procurement)", "2.1", date(2026, 4, 10)),
    Process("PR02", "Expense Approval", "M. Krause (Finance)", "1.4", date(2026, 6, 1)),
]

PROCESS_STEPS: list[ProcessStep] = [
    # Supplier Onboarding (PR01)
    ProcessStep("S01", "PR01", "start", "Onboarding request received", "Procurement Analyst", {"": "S02"}),
    ProcessStep("S02", "PR01", "task", "Verify supplier compliance documents", "Procurement Analyst", {"": "S03"}),
    ProcessStep("S03", "PR01", "decision", "Documents complete?", "Procurement Analyst", {"yes": "S04", "no": "S02"}),
    ProcessStep("S04", "PR01", "task", "Create supplier record in ERP", "Procurement Analyst", {"": "S05"}),
    ProcessStep("S05", "PR01", "task", "Process Owner sign-off", "Process Owner", {"": "S06"}),
    ProcessStep("S06", "PR01", "end", "Supplier active", "Procurement Analyst", {}),

    # Expense Approval (PR02)
    ProcessStep("E01", "PR02", "start", "Expense submitted", "Employee", {"": "E02"}),
    ProcessStep("E02", "PR02", "decision", "Amount over EUR 500?", "Finance System", {"yes": "E03", "no": "E04"}),
    ProcessStep("E03", "PR02", "task", "Manager approval required", "Manager", {"": "E04"}),
    ProcessStep("E04", "PR02", "task", "Finance review", "Finance Analyst", {"": "E05"}),
    ProcessStep("E05", "PR02", "end", "Expense reimbursed", "Finance Analyst", {}),
]

CHANGE_REQUESTS: list[ChangeRequest] = [
    ChangeRequest("CR01", "PR01", "J. Reyes", "Add a step for tax-ID validation before ERP record creation", "implemented", date(2026, 3, 1)),
    ChangeRequest("CR02", "PR02", "M. Krause", "Lower manager-approval threshold from EUR 1000 to EUR 500", "implemented", date(2026, 5, 20)),
    ChangeRequest("CR03", "PR01", "T. Nwosu", "Clarify which team owns re-verification after 12 months", "in_review", date(2026, 6, 15)),
    # Deliberately references a process that doesn't exist -- exercises
    # the validation logic in validation.py.
    ChangeRequest("CR04", "PR99", "A. Singh", "Add escalation path for rejected onboarding", "submitted", date(2026, 6, 18)),
]
