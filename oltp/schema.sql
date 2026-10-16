-- OLTP schema: ecommerce source of truth
CREATE TABLE IF NOT EXISTS orders (
  id SERIAL PRIMARY KEY,
  order_date DATE NOT NULL,
  amount NUMERIC(10,2) NOT NULL CHECK (amount > 0),
  status VARCHAR(20) NOT NULL DEFAULT 'completed'
);
CREATE INDEX IF NOT EXISTS idx_orders_date_status ON orders(order_date, status);
