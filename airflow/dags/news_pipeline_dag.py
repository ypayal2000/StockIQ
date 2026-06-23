from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="news_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["stockiq", "news"],
) as dag:

    run_news_pipeline = BashOperator(
        task_id="run_news_pipeline",
        bash_command="""
        cd /opt/airflow &&
        python -m src.sentiment.save_sentiment
        """
    )

    run_news_pipeline