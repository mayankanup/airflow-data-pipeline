# Plan — foundations (2026-10-16)
Phase: Phase 1 Foundations remainder (`specs/roadmap.md:5-9`). Schemas + seed scripts exist; missing `docker-compose.yml` + verification.

## 1. Compose file — full stack
- [ ] Add `docker-compose.yml`: `oltp-postgres:16`, `olap-postgres:16`, `airflow-webserver`, `airflow-scheduler`, `postgres-meta` per `specs/tech-stack.md:9`
- [ ] Pin ports/volumes: OLTP 5433->5432, OLAP 5434->5432, Airflow 8080; named volumes for data persistence
- [ ] Add `.env.example`: `OLTP_DSN`, `OLAP_DSN`, `AIRFLOW_*`
- Verify: `docker compose config` passes

## 2. Env wiring — connect existing code
- [ ] Ensure `oltp/schema.sql`, `olap/schema.sql`, `scripts/seed_15_days.py --clean`, `scripts/simulate_orders.py` work against compose DSNs
- [ ] Document DSNs in README snippet (localhost ports)
- Verify: `python scripts/seed_15_days.py --help` + `python scripts/simulate_orders.py --help` still pass

## 3. Up + verify — seed match
- [ ] `docker compose up -d`, wait healthy, run schemas + `seed_15_days.py --days 15 --clean`
- [ ] Check OLTP 15 days of orders present, OLAP `daily_sales_summary` rebuilt
- Verify: OLAP counts match OLTP `WHERE status='completed'` (see validations.md)
