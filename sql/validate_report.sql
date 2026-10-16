-- Validation oracle (OLTP source of truth). Compare per-date vs daily_sales_report.sql.
-- Full history (default):
SELECT order_date AS date, SUM(amount) AS total_revenue, COUNT(*) AS order_count
FROM orders
WHERE status = 'completed'
GROUP BY 1
ORDER BY 1;
-- Single-day spot check (psql): psql -v report_date='2026-10-15' -f sql/validate_report.sql
-- SELECT SUM(amount) AS total_revenue, COUNT(*) AS order_count
-- FROM orders
-- WHERE status = 'completed' AND order_date = :'report_date'::date;
