"""Validate Phase 5: RO user sees 15 chart points, cannot write."""
import psycopg2

RO_DSN = "dbname=olap user=metabase_reader password=metabase_reader host=localhost port=5434"

conn = psycopg2.connect(RO_DSN)
try:
    with conn.cursor() as c:
        c.execute("SELECT date, total_revenue, order_count FROM daily_sales_summary ORDER BY 1")
        rows = c.fetchall()
    print(f"RO SELECT rows={len(rows)} (expect 15 for chart)")
    assert len(rows) == 15, f"expected 15, got {len(rows)}"
    try:
        with conn.cursor() as c:
            c.execute("INSERT INTO daily_sales_summary(date, total_revenue, order_count) VALUES ('2000-01-01', 1, 1)")
        print("FAIL: RO INSERT succeeded (should be denied)")
        raise SystemExit(1)
    except psycopg2.errors.InsufficientPrivilege:
        conn.rollback()
        print("RO INSERT denied (expected)")
    try:
        with conn.cursor() as c:
            c.execute("DELETE FROM daily_sales_summary WHERE date='2000-01-01'")
        print("FAIL: RO DELETE succeeded (should be denied)")
        raise SystemExit(1)
    except psycopg2.errors.InsufficientPrivilege:
        conn.rollback()
        print("RO DELETE denied (expected)")
    print("METABASE-RO OK: chart query works, write blocked")
finally:
    conn.close()
