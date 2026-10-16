# Requirements — metabase-bi
Phase: `specs/roadmap.md:27-28` Phase 5 BI. Guidance: `specs/mission.md` (revenue summary `date,total_revenue,order_count`), `specs/tech-stack.md` (OLAP Postgres 16 `olap.daily_sales_summary`, all infra in compose).

## Scope
- In: `metabase` service on `:3000`, RO access to OLAP only, one saved chart `Daily Revenue` (`date` x `total_revenue`).
- Out: No auto-provisioned dashboards/JSON in git, no OLTP access, no products/categories, no auth SSO, no embedding.

## Decisions
- Compose + RO user (per answer): `metabase/metabase:latest`, `metabase-data` volume, new pg role `metabase_reader` with `GRANT SELECT` only — never reuse `postgres` superuser.
- Minimal BI (per answer): manual UI setup, no API provisioning; keeps Phase 5 tiny and reversible.
- OLAP host from Metabase container: `olap-postgres:5432`, db `olap` (from host laptop: `localhost:5434`).

## Context
- Existing: `olap-postgres` on 5434 with 15 rows `daily_sales_summary`, `scripts/validate_foundations.py` as truth.
- Missing: BI service, RO role SQL, setup docs.

## Non-Goals
- No DAG changes, no report SQL (Phase 3), no schedule changes (Phase 4).
