# Tech Stack — Locked for PoC

## Decision: Postgres OLTP -> Postgres OLAP + Airflow
Chosen per constitution: realistic, minimal infra, easy OLTP vs OLAP separation.

## Components
- **OLTP:** Postgres 16, db `oltp`, table `orders` (id, order_date, amount, status)
- **OLAP:** Postgres 16 (separate db/host), db `olap`, table `daily_sales_summary` (date PK, total_revenue, order_count)
- **Orchestration:** Apache Airflow 2.x in Docker (docker-compose: webserver, scheduler, postgres-meta)
- **Pipeline Code:** Python 3.11, `psycopg2-binary` / `SQLAlchemy`, Airflow `PostgresHook` / `PostgresOperator`
- **Local Dev:** Docker Compose, `.env` for connections, no cloud dependency

## Principles
- Separate OLTP / OLAP connections; no cross-db writes outside DAG.
- ELT-lite: Extract -> Load staging -> Aggregate SQL in OLAP.
- Idempotent loads: `DELETE + INSERT` or `ON CONFLICT DO UPDATE` on date.
- All infra as code in `docker-compose.yml`.
