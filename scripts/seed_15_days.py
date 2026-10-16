"""Seed past 15 days in OLTP + rebuild OLAP summary to match (PoC bootstrap).

Usage:
  python scripts/seed_15_days.py --days 15 --min-per-day 10 --max-per-day 40 --seed 42
Env:
  OLTP_DSN, OLAP_DSN
"""
import argparse, os, random
from datetime import date, timedelta
import psycopg2

OLTP_SCHEMA = open(os.path.join(os.path.dirname(__file__), "..", "oltp", "schema.sql")).read()
OLAP_SCHEMA = open(os.path.join(os.path.dirname(__file__), "..", "olap", "schema.sql")).read()

def get_dates(days: int):
    today = date.today()
    # past `days` full days, excluding today (mimics daily DAG processing yesterday)
    return [today - timedelta(days=i) for i in range(days, 0, -1)]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--days", type=int, default=15)
    p.add_argument("--min-per-day", type=int, default=10)
    p.add_argument("--max-per-day", type=int, default=40)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--clean", action="store_true", help="delete existing rows for target dates first")
    p.add_argument("--oltp-dsn", default=os.getenv("OLTP_DSN", "dbname=oltp user=postgres password=postgres host=localhost"))
    p.add_argument("--olap-dsn", default=os.getenv("OLAP_DSN", "dbname=olap user=postgres password=postgres host=localhost"))
    a = p.parse_args()
    rnd = random.Random(a.seed)
    dates = get_dates(a.days)

    oltp = psycopg2.connect(a.oltp_dsn)
    olap = psycopg2.connect(a.olap_dsn)
    try:
        with oltp, oltp.cursor() as cur:
            cur.execute(OLTP_SCHEMA)
            if a.clean:
                cur.execute("DELETE FROM orders WHERE order_date = ANY(%s)", (dates,))
        total = 0
        with oltp, oltp.cursor() as cur:
            for d in dates:
                n = rnd.randint(a.min_per_day, a.max_per_day)
                for _ in range(n):
                    amount = round(rnd.uniform(10, 500), 2)
                    status = "completed" if rnd.random() < 0.9 else rnd.choice(["pending", "cancelled"])
                    cur.execute(
                        "INSERT INTO orders(order_date, amount, status) VALUES (%s,%s,%s)",
                        (d, amount, status),
                    )
                total += n
        # Rebuild OLAP from OLTP so both stay consistent
        with olap, olap.cursor() as cur:
            cur.execute(OLAP_SCHEMA)
            cur.execute("DELETE FROM daily_sales_summary WHERE date = ANY(%s)", (dates,))
        # Fetch aggregates from OLTP and load into OLAP (keeps DBs separate)
        with oltp, oltp.cursor() as cur:
            cur.execute(
                """
                SELECT order_date, SUM(amount), COUNT(*)
                FROM orders WHERE status='completed' AND order_date = ANY(%s)
                GROUP BY 1 ORDER BY 1
                """,
                (dates,),
            )
            agg = cur.fetchall()
        with olap, olap.cursor() as cur:
            for d, rev, cnt in agg:
                cur.execute(
                    """
                    INSERT INTO daily_sales_summary(date, total_revenue, order_count)
                    VALUES (%s,%s,%s)
                    ON CONFLICT (date) DO UPDATE SET total_revenue=EXCLUDED.total_revenue, order_count=EXCLUDED.order_count
                    """,
                    (d, rev, cnt),
                )
        print(f"seeded {total} OLTP orders across {len(dates)} days ({dates[0]}..{dates[-1]})")
        print(f"rebuilt {len(agg)} OLAP summary rows")
    finally:
        oltp.close()
        olap.close()

if __name__ == "__main__":
    main()
