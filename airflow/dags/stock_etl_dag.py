from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="stock_etl_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["stockiq"],
) as dag:

    run_pipeline = BashOperator(
        task_id="run_stock_pipeline",
        bash_command="""
        cd /opt/airflow &&
        python src/main.py
        """
    )