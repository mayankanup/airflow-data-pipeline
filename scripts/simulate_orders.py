"""On-demand order simulator for OLTP. Appends random orders for a given date."""
import argparse, os, random
from datetime import date
import psycopg2

def simulate(dsn: str, order_date: str, count: int, seed: int | None = None):
    rnd = random.Random(seed)
    conn = psycopg2.connect(dsn)
    try:
        with conn, conn.cursor() as cur:
            for _ in range(count):
                amount = round(rnd.uniform(10, 500), 2)
                # 90% completed so report filter is exercised
                status = "completed" if rnd.random() < 0.9 else rnd.choice(["pending", "cancelled"])
                cur.execute(
                    "INSERT INTO orders(order_date, amount, status) VALUES (%s,%s,%s)",
                    (order_date, amount, status),
                )
    finally:
        conn.close()
    print(f"inserted {count} orders for {order_date}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--date", default=str(date.today()), help="YYYY-MM-DD")
    p.add_argument("--count", type=int, default=20)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--dsn", default=os.getenv("OLTP_DSN", "dbname=oltp user=postgres password=postgres host=localhost"))
    a = p.parse_args()
    simulate(a.dsn, a.date, a.count, a.seed)
