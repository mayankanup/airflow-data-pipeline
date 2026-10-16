# Validations — foundations
Merge gate for `feature/2026-10-16-foundations`. Must all be green.

## Success Checks
1. `docker compose config` → no errors, 5 services listed
2. `docker compose up -d` → `docker ps` shows healthy oltp/olap/meta + airflow webserver/scheduler
3. `python scripts/seed_15_days.py --days 15 --clean --seed 42` → prints `seeded ~375 OLTP orders across 15 days` + `rebuilt 15 OLAP summary rows`
4. OLAP vs OLTP match:
   ```sql
   -- OLTP (psql oltp, port 5433):
   SELECT order_date, SUM(amount), COUNT(*) FROM orders
   WHERE status='completed' GROUP BY 1 ORDER BY 1;
   -- OLAP (psql olap, port 5434):
   SELECT date, total_revenue, order_count FROM daily_sales_summary ORDER BY 1;
   ```
   → row counts equal (15), per-date revenue/count equal
5. Rerun: `python scripts/seed_15_days.py --days 15 --clean` twice → second run same 15 rows, no dupes (upsert/delete+insert holds)

## Merge Gate
- [ ] all 5 checks green
- [ ] `plan.md` all boxes checked
- [ ] no changes to `specs/mission.md` / `specs/tech-stack.md` scope
- [ ] branch `feature/2026-10-16-foundations` ready to merge to `main`
