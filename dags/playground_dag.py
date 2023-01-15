from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from utils.datasystem.base import DataSystem

from datetime import datetime

data_system = DataSystem()


def playground_function():
    buckets = data_system.list_buckets()
    print(buckets)


with DAG(
    dag_id="playground_dag", start_date=datetime(2022, 5, 28), schedule_interval=None
) as dag:

    start_task = EmptyOperator(task_id="start")

    python_task = PythonOperator(
        task_id="playground_task", python_callable=playground_function
    )

start_task >> python_task
