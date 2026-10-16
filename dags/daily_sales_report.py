"""Phase 2: daily sales report DAG — extract yesterday from OLTP, upsert to OLAP."""
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook


def extract(ds=None, ti=None):
    hook = PostgresHook(postgres_conn_id="oltp_default")
    rows = hook.get_records(
        """
        SELECT COALESCE(SUM(amount), 0), COUNT(*)
        FROM orders WHERE order_date = %s AND status = 'completed'
        """,
        parameters=(ds,),
    )
    total, cnt = rows[0]
    ti.xcom_push(key="report_date", value=ds)
    ti.xcom_push(key="total_revenue", value=float(total))
    ti.xcom_push(key="order_count", value=int(cnt))
    print(f"extract {ds}: revenue={total} count={cnt}")
    return {"report_date": ds, "total_revenue": float(total), "order_count": int(cnt)}


def load(ds=None, ti=None):
    data = ti.xcom_pull(task_ids="extract", key="return_value") or {
        "report_date": ti.xcom_pull(task_ids="extract", key="report_date"),
        "total_revenue": ti.xcom_pull(task_ids="extract", key="total_revenue"),
        "order_count": ti.xcom_pull(task_ids="extract", key="order_count"),
    }
    hook = PostgresHook(postgres_conn_id="olap_default")
    hook.run(
        """
        INSERT INTO daily_sales_summary(date, total_revenue, order_count)
        VALUES (%s, %s, %s)
        ON CONFLICT (date) DO UPDATE SET
          total_revenue = EXCLUDED.total_revenue,
          order_count = EXCLUDED.order_count
        """,
        parameters=(data["report_date"], data["total_revenue"], data["order_count"]),
    )
    print(f"load {data['report_date']}: revenue={data['total_revenue']} count={data['order_count']}")


with DAG(
    dag_id="daily_sales_report",
    start_date=datetime(2026, 10, 1),
    schedule="@daily",
    catchup=False,
    tags=["poc", "sales"],
) as dag:
    t_extract = PythonOperator(task_id="extract", python_callable=extract)
    t_load = PythonOperator(task_id="load", python_callable=load)
    t_extract >> t_load
