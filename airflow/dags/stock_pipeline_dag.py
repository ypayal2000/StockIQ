from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.main import run_pipeline
from src.spark.stock_analytics import run_analytics


default_args = {
    "owner": "stockiq"
}


with DAG(
    dag_id="stock_pipeline",
    default_args=default_args,
    start_date=datetime(2026, 6, 19),
    schedule="@daily",
    catchup=False,
) as dag:

    etl_task = PythonOperator(
        task_id="etl_pipeline",
        python_callable=run_pipeline
    )

    analytics_task = PythonOperator(
        task_id="spark_analytics",
        python_callable=run_analytics
    )

    etl_task >> analytics_task