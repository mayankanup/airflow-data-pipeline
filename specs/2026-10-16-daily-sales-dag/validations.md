# Validations — daily-sales-dag
Merge gate for `feature/2026-10-16-daily-sales-dag`. Must all be green.

## Success Checks
1. `docker compose exec airflow-scheduler airflow dags list` → includes `daily_sales_report`
2. `airflow dags trigger daily_sales_report --conf '{"date":"2026-10-15"}'` or UI trigger with `ds=2026-10-15` → both tasks succeed (logs show extract aggregates + load upsert)
3. OLAP row correct:
   ```sql
   SELECT date, total_revenue, order_count FROM daily_sales_summary WHERE date='2026-10-15';
   ```
   → equals OLTP `SELECT SUM(amount), COUNT(*) FROM orders WHERE order_date='2026-10-15' AND status='completed'`
4. Rerun same `ds` → still 1 row for date, values identical, no dupes (`SELECT COUNT(*) ... WHERE date='2026-10-15'` = 1)
5. `python scripts/validate_foundations.py` still MATCH (no regression on 15-day seed)

## Merge Gate
- [ ] all 5 checks green
- [ ] `plan.md` boxes checked (extract + load verified)
- [ ] no changes to `specs/mission.md` / `specs/tech-stack.md` scope
- [ ] branch `feature/2026-10-16-daily-sales-dag` ready to merge
