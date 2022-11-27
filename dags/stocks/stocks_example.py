from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

from stocks.functions import fetch_price_data

#
# DAG default arguments
#
default_args = {
    "depends_on_past": False,
    "retries": 1,
}

#
# Setup Airflow DAG
#
dag = DAG(
    dag_id="stocks_example",
    default_args=default_args,
    description="Sample dag to simulate simple extract, transform, load on stock market data, runs every morning at 6am",
    catchup=False,
    start_date=datetime(2022, 10, 7),
    schedule_interval="0 6 * * *",
)

#
# Airflow operations
#
fetch_data = PythonOperator(
    task_id="fetch_data", python_callable=fetch_price_data, dag=dag
)


#
# Setup operation flow
#
fetch_data
