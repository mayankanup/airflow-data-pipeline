# Validations — report-query
Merge gate for `feature/2026-10-16-report-query`. Must all be green.

## Success Checks
1. `sql/daily_sales_report.sql` runs on OLAP → 15 rows ordered by date
2. `sql/validate_report.sql` runs on OLTP → 15 aggregates, per-date revenue/count equal to report output
3. Single-date param: both queries with `:report_date='2026-10-15'` return identical 1 row
4. `python scripts/validate_foundations.py` → still MATCH (no regression)
5. Cross-check Metabase: `Daily Revenue` card (id 40, `http://localhost:3000/question/40`) shows same 15 points / same `2026-10-15` values (`6160.27` / `22`)

## Merge Gate
- [ ] all 5 checks green
- [ ] `plan.md` boxes checked
- [ ] no changes to `specs/mission.md` / `specs/tech-stack.md` scope
- [ ] branch `feature/2026-10-16-report-query` ready to merge
