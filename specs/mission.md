# Mission — Daily Sales Report PoC

## Purpose
Prove daily data transfer from OLTP (ecommerce app) to OLAP (reporting) to generate a daily sales report.

## PoC Scope: Revenue Summary Only
- In scope: `date`, `total_revenue`, `order_count` per day.
- Source: OLTP `orders` table (completed orders only).
- Destination: OLAP `daily_sales_summary` table.
- Grain: one row per calendar date.

## Success Criteria
1. Airflow DAG runs daily, extracts yesterday's orders from OLTP.
2. Loads/aggregates into OLAP `daily_sales_summary`.
3. Report query returns correct revenue + count vs OLTP source.
4. Re-runnable / idempotent for same date (no duplicates).

## Non-Goals (Out of PoC)
- No top products, categories, customers, returns, inventory.
- No real-time / intraday, no backfill UI, no BI dashboard.
- No performance tuning, no PII handling.
