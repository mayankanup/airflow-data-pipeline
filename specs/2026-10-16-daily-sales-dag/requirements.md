# Requirements — daily-sales-dag
Phase: `specs/roadmap.md:11-15` Phase 2. Guidance: `specs/mission.md` (grain 1 row/date, `completed` only, idempotent reruns), `specs/tech-stack.md` (Airflow 2.x Docker, `PostgresHook`, `ON CONFLICT DO UPDATE`).

## Scope
- In: `dags/daily_sales_report.py` with 2 tasks (`extract` OLTP, `load` OLAP), connections `oltp_default` + `olap_default` (already in compose), `@daily` targeting `{{ ds }}`.
- Out: No `sql/daily_sales_report.sql` (Phase 3), no schedule/backfill harness (Phase 4), no products/categories, no TaskFlow/dynamic mapping.

## Decisions
- Hook + upsert (per answer): `PythonOperator` + `PostgresHook` over SQL-only operators for explicit XCom + testability.
- Two-task ETL (per answer): separate `extract` / `load` to isolate OLTP read vs OLAP write failures, preserve `extract >> load` order.
- Idempotency: `load` uses `INSERT ... ON CONFLICT (date) DO UPDATE SET total_revenue, order_count`; `extract` is read-only.

## Context
- Existing: compose connections (`AIRFLOW_CONN_OLTP_DEFAULT`, `AIRFLOW_CONN_OLAP_DEFAULT`), `oltp/schema.sql`, `olap/schema.sql`, `scripts/validate_foundations.py` as oracle.
- Missing: DAG file; `dags/` currently empty (UI shows none).

## Non-Goals
- No intraday/real-time, no BI, no PII (per `specs/mission.md:18-21`).
