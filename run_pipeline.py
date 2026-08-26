"""
Runs the full process-documentation-toolkit pipeline end to end: loads
the structured process register, runs integrity checks, summarizes
change requests, and renders a real flowchart PNG for each process.
Prints a real console report.
"""

from src.change_requests import oldest_open_request, open_requests, summarize_by_status
from src.flowchart import render_flowchart_png
from src.process_model import CHANGE_REQUESTS, PROCESS_STEPS, PROCESSES
from src.validation import run_all_checks


def main():
    print(f"Loaded {len(PROCESSES)} processes, {len(PROCESS_STEPS)} process steps, "
          f"{len(CHANGE_REQUESTS)} change requests.\n")

    checks = run_all_checks(PROCESS_STEPS, PROCESSES, CHANGE_REQUESTS)
    print("Process integrity checks:")
    print(f"  Dangling step references: {checks['dangling_step_references']}")
    print(f"  Orphaned change requests: {[r.request_id for r in checks['orphaned_change_requests']]}")
    print(f"  Processes without a reachable end: {checks['processes_without_reachable_end']}\n")

    print("Change request status summary:")
    for status, count in summarize_by_status(CHANGE_REQUESTS).items():
        print(f"  {status}: {count}")

    oldest = oldest_open_request(CHANGE_REQUESTS)
    print(f"\nOldest open change request: {oldest.request_id if oldest else 'none'} "
          f"({oldest.description if oldest else ''})")

    print(f"\nOpen requests ({len(open_requests(CHANGE_REQUESTS))}):")
    for r in open_requests(CHANGE_REQUESTS):
        print(f"  {r.request_id} [{r.process_id}] {r.description} (status={r.status})")

    print("\nRendering flowcharts:")
    for process in PROCESSES:
        path = render_flowchart_png(PROCESS_STEPS, process.process_id, process.name, f"output/{process.process_id}_flowchart")
        print(f"  {process.process_id} ({process.name}) -> {path}")


if __name__ == "__main__":
    main()
