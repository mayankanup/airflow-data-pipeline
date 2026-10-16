# Plan — daily-sales-dag (2026-10-16)
Phase: Phase 2 Extract + Load DAG (`specs/roadmap.md:11-15`). Foundations done (compose + seed verified).

## 1. Extract — yesterday from OLTP
- [ ] Add `dags/daily_sales_report.py`: DAG id `daily_sales_report`, `@daily`, `catchup=False`, task `extract` (PythonOperator + `PostgresHook` `oltp_default`)
- [ ] Query OLTP: `SELECT SUM(amount), COUNT(*) FROM orders WHERE order_date = '{{ ds }}' AND status='completed'` (yesterday via `ds`)
- [ ] Push `total_revenue`, `order_count`, `report_date` via XCom
- Verify: `airflow dags list` shows DAG, `airflow tasks test daily_sales_report extract <date>` returns correct aggregates

## 2. Load — upsert to OLAP
- [ ] Task `load` (PythonOperator + `PostgresHook` `olap_default`): `INSERT ... ON CONFLICT (date) DO UPDATE` into `daily_sales_summary`
- [ ] Set `extract >> load`, retries 1, no cross-db writes outside tasks
- Verify: manual trigger creates 1 correct row; rerun same `ds` updates same row, no dupes
