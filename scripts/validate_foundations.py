"""Validate foundations: OLAP matches OLTP. Used by validations.md check 4+5."""
import os
import psycopg2

OLTP_DSN = os.getenv("OLTP_DSN", "dbname=oltp user=postgres password=postgres host=localhost port=5433")
OLAP_DSN = os.getenv("OLAP_DSN", "dbname=olap user=postgres password=postgres host=localhost port=5434")

oltp = psycopg2.connect(OLTP_DSN)
olap = psycopg2.connect(OLAP_DSN)
try:
    with oltp.cursor() as c:
        c.execute("""
            SELECT order_date, SUM(amount), COUNT(*)
            FROM orders WHERE status='completed'
            GROUP BY 1 ORDER BY 1
        """)
        a = c.fetchall()
    with olap.cursor() as c:
        c.execute("SELECT date, total_revenue, order_count FROM daily_sales_summary ORDER BY 1")
        b = c.fetchall()
    print(f"OLTP days={len(a)} OLAP rows={len(b)}")
    mism = [(x, y) for x, y in zip(a, b)
            if str(x[0]) != str(y[0]) or float(x[1]) != float(y[1]) or x[2] != y[2]]
    if mism or len(a) != len(b):
        print("MISMATCHES:", mism)
        raise SystemExit(1)
    print("MATCH: all per-date revenue/count equal, 15 rows")
finally:
    oltp.close()
    olap.close()
