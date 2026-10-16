# Plan — report-query (2026-10-16)
Phase: Phase 3 Report Query (`specs/roadmap.md:17-20`). DAG + seed live on `main`.

## 1. Report SQL — OLAP daily sales
- [ ] Add `sql/daily_sales_report.sql`: `SELECT date, total_revenue, order_count FROM daily_sales_summary ORDER BY date` with optional `:report_date` param filter
- [ ] Keep grain 1 row/date per `specs/mission.md:10`
- Verify: runs on OLAP (`localhost:5434`), returns 15 rows

## 2. Validation query — OLTP oracle
- [ ] Add `sql/validate_report.sql`: OLTP aggregate `SELECT order_date, SUM(amount), COUNT(*) FROM orders WHERE status='completed' GROUP BY 1 ORDER BY 1`
- [ ] Document param variant `WHERE order_date = :report_date` for single-day check
- Verify: per-date revenue/count equal vs report SQL

## 3. Run + compare — prove match
- [ ] Run both queries, diff output (reuse `scripts/validate_foundations.py` as runner reference)
- [ ] Note Metabase cross-check: `Daily Revenue` card (id 40) shows same 15 points
- Verify: full 15-day MATCH, no drift
