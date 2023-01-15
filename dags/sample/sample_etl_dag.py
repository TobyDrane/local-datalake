from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
from airflow.utils.dates import days_ago

from datetime import datetime, timedelta

from utils.datasystem.base import DataSystem
from dags.sample.functions import extract_user

default_args = {
    "depends_on_past": False,
    "start_date": days_ago(1),
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="sample_etl_dag",
    default_args=default_args,
    schedule_interval=timedelta(days=1),
) as dag:

    with TaskGroup("extract") as extract_group:
        extract_user_data_task = PythonOperator(
            task_id="extract_user_data",
            python_callable=extract_user,
            op_kwargs={"amount": 10},
        )

extract_group
