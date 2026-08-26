# Process Documentation Toolkit

A real, tested Python project that models a structured business-process
register — typed process steps, a change-request workflow, integrity
validation, and real flowchart rendering — built specifically for
Infineon's "Working Student - Business Process Management" posting,
whose exact task list (support/coordinate processes, document business
processes in a professional tool, editorial work and graphical
representation of processes, take over documentation/implementation
requests) had no prior evidence anywhere in this portfolio.

## What this is (read before citing anywhere)

**All process content is invented.** `src/process_model.py` defines two
fictional processes (Supplier Onboarding, Expense Approval) modeled
loosely on plausible enterprise workflows, with steps, owners, and a
handful of realistic change requests — none of it reflects any real
Infineon process, tool, or data.

**This uses Graphviz, not a licensed enterprise process-modeling tool.**
The posting names "documentation... in a professional tool," which most
naturally means something like Signavio, ARIS, or Visio — none of which
were available or licensable in this build environment. `src/flowchart.py`
renders real, working flowchart images from the structured process data
using open-source Graphviz instead. This demonstrates the underlying
skill (turning a structured process definition into a correct, legible
graphical representation, and catching a broken definition before it's
published) honestly, not a claim of hands-on experience with a specific
commercial BPM tool.

## What it actually does

- **`src/process_model.py`** — typed process steps (start/task/
  decision/end) with owners and defined flow, a process register, and a
  change-request log, including one deliberately dangling change
  request (referencing a process that doesn't exist), so the validation
  logic has a real problem to catch.
- **`src/validation.py`** — three integrity checks: dangling step
  references (a step pointing to a step id that doesn't exist),
  orphaned change requests (referencing an unknown process), and
  reachability (does every process actually have a path from its start
  step to an end step, via breadth-first traversal through decision
  branches) — the kind of "keep the overview" correctness a process
  register needs so a documented flow can't silently drift into
  something unnavigable.
- **`src/change_requests.py`** — filtering and summarizing change
  requests by status, and finding the oldest open request — the
  "requests for documentation and implementation" workflow the posting
  names, made queryable rather than an unordered list.
- **`src/flowchart.py`** — renders a process's steps as a real PNG
  flowchart via Graphviz, with shape/color conventions for start, task,
  decision, and end steps, and labeled decision branches.
- **`run_pipeline.py`** — runs the full flow end to end, prints a real
  console report, and writes real PNG flowcharts to `output/` (see
  sample output below, copied from an actual run).

## Verification

21 automated tests (`tests/`), all passing on the first run — stated
honestly rather than inventing a bug: the reachability check in
particular was written test-first against several deliberately broken
flows (an infinite loop, a missing start step) before being run against
the real process data, which likely caught issues before they became
test failures.

```bash
python3 -m pytest -v      # 21 tests, all passing
python3 run_pipeline.py   # runs the full pipeline, writes output/*.png
```

## Sample output (from an actual run)

```
Loaded 2 processes, 11 process steps, 4 change requests.

Process integrity checks:
  Dangling step references: []
  Orphaned change requests: ['CR04']
  Processes without a reachable end: []

Change request status summary:
  implemented: 2
  in_review: 1
  submitted: 1

Oldest open change request: CR03 (Clarify which team owns re-verification after 12 months)

Open requests (2):
  CR03 [PR01] Clarify which team owns re-verification after 12 months (status=in_review)
  CR04 [PR99] Add escalation path for rejected onboarding (status=submitted)

Rendering flowcharts:
  PR01 (Supplier Onboarding) -> output/PR01_flowchart.png
  PR02 (Expense Approval) -> output/PR02_flowchart.png
```

`CR04` is correctly flagged as an orphaned change request — it
references process `PR99`, which doesn't exist in the register — while
every actual process step forms a complete, reachable start-to-end
path. The rendered PR01 flowchart shows a genuinely correct diagram,
including the "no" branch looping back to re-verify documents before
proceeding.

## Honest limitations

- All process, step, and change-request data is synthetic — no real
  Infineon process documentation was accessed or used.
- Diagrams are rendered with open-source Graphviz, not a licensed
  enterprise process-modeling tool — the underlying skill (correct,
  legible graphical process representation from structured data) is
  real and demonstrated, but this is not a claim of Signavio/ARIS/Visio
  experience specifically.
- The process model is intentionally simple (linear steps and binary
  decisions) — a production business-process tool would need to handle
  parallel branches, sub-processes, and swimlanes, which this project
  does not attempt.
