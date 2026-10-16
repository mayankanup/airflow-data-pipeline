# Roadmap — Implementation Order

Very small phases, each independently verifiable. Stop after Phase 4 for PoC complete.

## Phase 1: Foundations
- Add `docker-compose.yml` (Airflow + oltp-postgres + olap-postgres)
- Create OLTP schema `orders` + seed script with sample data
- Create OLAP schema `daily_sales_summary`
- Verify: both DBs reachable, seed counts match

## Phase 2: Extract + Load DAG
- Single DAG `daily_sales_report` @daily, one task: aggregate yesterday from OLTP
- Use Airflow Connections `oltp_default`, `olap_default`
- Idempotent write to OLAP (delete/insert or upsert by date)
- Verify: manual DAG run creates 1 correct row in OLAP

## Phase 3: Report Query
- Add `sql/daily_sales_report.sql`: SELECT date, total_revenue, order_count ORDER BY date
- Add validation query comparing OLAP vs OLTP aggregate
- Verify: report output matches source of truth

## Phase 4: Validate + Schedule
- Enable schedule, test rerun/backfill for same date (no dupes)
- Add README run instructions + sample output
- PoC done gate: 3 consecutive daily runs green

## Future (Out of PoC)
- Phase 5+: products/categories, incremental CDC, BI, tests/CI.
