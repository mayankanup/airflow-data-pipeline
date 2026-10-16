# Requirements — report-query
Phase: `specs/roadmap.md:17-20` Phase 3. Guidance: `specs/mission.md` (scope `date,total_revenue,order_count`, `completed` only), `specs/tech-stack.md` (OLAP `olap.daily_sales_summary`, OLTP `oltp.orders`).

## Scope
- In: `sql/daily_sales_report.sql` (OLAP, ordered by date, optional `:report_date` filter), `sql/validate_report.sql` (OLTP oracle aggregate).
- Out: No DAG changes (Phase 2 done), no schedule/backfill (Phase 4), no new tables, no BI provisioning changes.

## Decisions
- Parametrized date (per answer): both SQL files support full-history default plus `:report_date` single-day filter for spot checks.
- OLAP is source for report; OLTP aggregate is oracle only — never write from report queries (principle `specs/tech-stack.md:14`).
- Keep SQL plain Postgres, no extensions; runnable via `psql -f` and Metabase native question.

## Context
- Existing: 15 seeded days `2026-10-01..2026-10-15`, DAG `daily_sales_report` upserting, Metabase card `Daily Revenue` (id 40).
- Missing: versioned SQL files under `sql/`.

## Non-Goals
- No CSV export automation, no scheduling, no PII (per `specs/mission.md:18-21`).
