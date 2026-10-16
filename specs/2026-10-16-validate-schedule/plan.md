# Plan — validate-schedule (2026-10-16)
Phase: Phase 4 Validate + Schedule (`specs/roadmap.md:22-25`). DAG, report SQL, and seed live on `main`. PoC done-gate phase.

## 1. Schedule on — daily runs green
- [ ] Confirm DAG `daily_sales_report` `schedule="@daily"`, `catchup=False` is unpaused in Airflow UI / `airflow dags unpause daily_sales_report`
- [ ] Let scheduler fire 3 consecutive daily runs (or trigger 3 runs for 3 distinct `ds` values)
- Verify: `airflow dags list-runs -d daily_sales_report` shows 3 `success`, UI grid all green

## 2. Rerun / backfill — no dupes
- [ ] Rerun same `ds` twice (`dags test` or UI re-trigger); run `sql/daily_sales_report.sql` after each
- [ ] Confirm per-date row count stays 1 (`SELECT COUNT(*) ... WHERE date='<ds>'` = 1) and values identical
- Verify: `python scripts/validate_foundations.py` still MATCH

## 3. README — run instructions + sample output
- [ ] Add `README.md`: compose up, seed 15 days, connections, trigger DAG, run report SQL, open Metabase chart; include sample output table (15 rows)
- [ ] Record PoC done-gate evidence (run IDs, dates, MATCH output)
- Verify: fresh-eyes run-through of README reproduces MATCH
