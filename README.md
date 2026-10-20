# airflow-data-pipeline — Daily Sales Report PoC

Proves daily data transfer from OLTP (ecommerce `orders`) to OLAP (`daily_sales_summary`) with Airflow. Scope: `specs/mission.md`. Stack: `specs/tech-stack.md` (Postgres 16 → Postgres 16 + Airflow 2.9 Docker).

## Architecture

![Architecture](docs/architecture.svg)

OLTP `orders` → Airflow batch ELT (`extract` → `load`, idempotent upsert) → OLAP `daily_sales_summary` → Metabase BI. SQL report + OLTP oracle live in `sql/`.

## Quickstart

```powershell
cp .env.example .env
docker compose up -d
docker compose exec airflow-scheduler airflow db migrate
docker compose exec airflow-scheduler airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
docker compose exec airflow-scheduler airflow connections add oltp_default --conn-uri postgres://postgres:postgres@oltp-postgres:5432/oltp
docker compose exec airflow-scheduler airflow connections add olap_default --conn-uri postgres://postgres:postgres@olap-postgres:5432/olap

$env:OLTP_DSN="dbname=oltp user=postgres password=postgres host=localhost port=5433"
$env:OLAP_DSN="dbname=olap user=postgres password=postgres host=localhost port=5434"
python scripts/seed_15_days.py --days 15 --clean --seed 42
python scripts/validate_foundations.py
```

Seed result: `seeded 420 OLTP orders across 15 days (2026-10-01..2026-10-15)`, `rebuilt 15 OLAP summary rows`.

## Run the DAG

```powershell
docker compose exec airflow-scheduler airflow dags unpause daily_sales_report
docker compose exec airflow-scheduler airflow dags backfill -s 2026-10-13 -e 2026-10-15 daily_sales_report
docker compose exec airflow-scheduler airflow dags list-runs -d daily_sales_report
```

Airflow UI: `http://localhost:8080` (admin/admin). Reruns are idempotent (upsert on `date`).

## Report

```powershell
Get-Content sql/daily_sales_report.sql | docker exec -i olap-postgres psql -U postgres -d olap
Get-Content sql/validate_report.sql | docker exec -i oltp-postgres psql -U postgres -d oltp
```

Sample output (both queries identical):

| date | total_revenue | order_count |
|---|---|---|
| 2026-10-01 | 5797.92 | 28 |
| 2026-10-02 | 7729.27 | 29 |
| 2026-10-03 | 6526.67 | 32 |
| 2026-10-04 | 7305.06 | 33 |
| 2026-10-05 | 4672.11 | 16 |
| 2026-10-06 | 8584.98 | 35 |
| 2026-10-07 | 8412.79 | 31 |
| 2026-10-08 | 5288.78 | 22 |
| 2026-10-09 | 7057.82 | 24 |
| 2026-10-10 | 4797.60 | 21 |
| 2026-10-11 | 8535.58 | 32 |
| 2026-10-12 | 3367.23 | 13 |
| 2026-10-13 | 5125.67 | 20 |
| 2026-10-14 | 5883.91 | 21 |
| 2026-10-15 | 6160.27 | 22 |

## BI (Phase 5, optional)

`docker compose up -d metabase` → `http://localhost:3000`. Add Postgres `olap-postgres:5432/olap` as `metabase_reader`/`metabase_reader` (see `olap/create_readonly_user.sql`). Open saved question **Daily Revenue** (`/question/40`).

## PoC done-gate evidence (2026-10-16)

- `list-runs`: `manual__2026-10-15`, `backfill__2026-10-13`, `backfill__2026-10-14` → all `success`
- Rerun `2026-10-15` → `COUNT(*)=1`, `6160.27/22` unchanged
- `validate_foundations.py` → `OLTP days=15 OLAP rows=15 MATCH`

## Layout

- `dags/` Airflow DAG, `sql/` report + oracle queries
- `oltp/`, `olap/` schemas, `scripts/` seed/simulate/validate
- `specs/` mission, tech-stack, roadmap, per-phase specs
