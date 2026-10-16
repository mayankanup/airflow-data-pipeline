-- Daily sales report (OLAP source of truth for BI).
-- Full history (default):
SELECT date, total_revenue, order_count
FROM daily_sales_summary
ORDER BY date;
-- Single-day spot check (psql): psql -v report_date='2026-10-15' -f sql/daily_sales_report.sql
-- SELECT date, total_revenue, order_count
-- FROM daily_sales_summary
-- WHERE date = :'report_date'::date;
