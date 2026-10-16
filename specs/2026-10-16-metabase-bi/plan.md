# Plan — metabase-bi (2026-10-16)
Phase: Phase 5 BI (extends `specs/roadmap.md:27-28` Future). Prior phases done (foundations + DAG on `main`).

## 1. Compose service — Metabase OSS
- [ ] Add `metabase` to `docker-compose.yml`: image `metabase/metabase:latest`, port `3000:3000`, volume `metabase-data`, `depends_on: olap-postgres`
- [ ] Persist appdb in named volume; document first-run setup at `http://localhost:3000`
- Verify: `docker compose config --services` includes `metabase`, `docker ps` healthy

## 2. Connect OLAP — read-only
- [ ] Create RO pg role on `olap` (e.g. `metabase RO SELECT on daily_sales_summary`), wire host `olap-postgres:5432`, db `olap`
- [ ] Document connection params in `.env.example` (`MB_DB_*` not needed; OLAP creds only)
- Verify: Metabase Add database → Postgres → Save succeeds, syncs `daily_sales_summary`

## 3. Chart — daily revenue
- [ ] In UI: New Question → `daily_sales_summary` → line/bar `total_revenue` by `date` (last 15 days), save as `Daily Revenue`
- [ ] Screenshot / note steps in `specs/2026-10-16-metabase-bi/` (no auto-provisioning)
- Verify: chart renders 15 points matching `validate_foundations.py`
