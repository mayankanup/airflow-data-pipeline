# Requirements — foundations
Phase: `specs/roadmap.md:5-9` Phase 1. Guidance: `specs/mission.md` (revenue summary only, `date,total_revenue,order_count`), `specs/tech-stack.md` (Postgres 16 -> Postgres 16 + Airflow 2.x Docker).

## Scope
- In: `docker-compose.yml` with 5 services: oltp-postgres, olap-postgres, airflow-webserver, airflow-scheduler, postgres-meta. `.env.example`. Up + seed + verify docs.
- Out: No DAG (Phase 2), no `sql/daily_sales_report.sql` (Phase 3), no schedule/backfill (Phase 4), no products/categories/BI.

## Decisions
- Full stack now (per answer): include Airflow services in compose even though DAG comes in Phase 2, to prove infra early.
- Separate DBs/hosts: `oltp` db on 5433, `olap` db on 5434, meta db internal only. No cross-db writes outside DAG (principle `specs/tech-stack.md:14`).
- ELT-lite + idempotent seed: existing `ON CONFLICT DO UPDATE` / `DELETE + INSERT` by date reused.

## Context
- Existing: `oltp/schema.sql` (`orders`), `olap/schema.sql` (`daily_sales_summary`), `scripts/seed_15_days.py`, `scripts/simulate_orders.py`, `requirements.txt` (`psycopg2-binary`).
- Missing: compose file, `.env.example`, verified up + seed match.

## Non-Goals
- No DAG logic, no report query, no performance tuning, no PII handling (per `specs/mission.md:18-21`).
