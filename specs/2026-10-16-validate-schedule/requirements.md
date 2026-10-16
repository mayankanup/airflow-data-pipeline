# Requirements — validate-schedule
Phase: `specs/roadmap.md:22-25` Phase 4. Guidance: `specs/mission.md` (success criteria 1-4: daily runs, correct report, idempotent reruns), `specs/tech-stack.md` (Airflow 2.x Docker, all infra in compose).

## Scope
- In: schedule enabled on `daily_sales_report`, rerun/backfill idempotency proof, `README.md` with run instructions + sample output, PoC done-gate record.
- Out: No DAG logic changes, no new SQL, no BI changes, no products/categories/CDC (Future per roadmap).

## Decisions
- Schedule plus gate (per answer): `@daily` stays on with `catchup=False`; done-gate is 3 consecutive green runs, not a one-off trigger.
- README is part of the gate: must let a fresh checkout reproduce compose → seed → DAG → report MATCH.
- Evidence over assertions: run IDs, per-date counts, and `validate_foundations.py` output recorded in README.

## Context
- Existing: compose (6 services incl. Metabase), `dags/daily_sales_report.py` (extract>>load, upsert), `sql/daily_sales_report.sql`, `sql/validate_report.sql`, `scripts/validate_foundations.py`, Metabase card 40.
- Missing: enabled schedule proof, rerun evidence, README.

## Non-Goals
- No backfill UI work, no real-time/intraday, no performance tuning, no PII (per `specs/mission.md:18-21`).
