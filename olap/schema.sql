-- OLAP schema: reporting target
CREATE TABLE IF NOT EXISTS daily_sales_summary (
  date DATE PRIMARY KEY,
  total_revenue NUMERIC(12,2) NOT NULL,
  order_count INT NOT NULL
);
