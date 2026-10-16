# Validations — validate-schedule
Merge gate for `feature/2026-10-16-validate-schedule`. Closes the PoC. Must all be green.

## Success Checks
1. `airflow dags list-runs -d daily_sales_report` (or UI grid) → 3 consecutive runs `success`
2. Rerun same `ds` twice → `SELECT COUNT(*) FROM daily_sales_summary WHERE date='<ds>'` stays 1, revenue/count unchanged
3. `sql/daily_sales_report.sql` (15 rows) equals `sql/validate_report.sql` output row-for-row
4. `python scripts/validate_foundations.py` → MATCH (no regression)
5. `README.md` exists with compose/seed/DAG/report/Metabase steps + sample 15-row output; follow-through reproduces MATCH

## Merge Gate
- [ ] all 5 checks green
- [ ] `plan.md` boxes checked (schedule + rerun + README)
- [ ] no changes to `specs/mission.md` / `specs/tech-stack.md` scope
- [ ] branch `feature/2026-10-16-validate-schedule` ready to merge — merging closes PoC per `specs/roadmap.md:3`
