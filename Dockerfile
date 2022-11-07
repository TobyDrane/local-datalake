FROM apache/airflow:2.3.0
USER airflow

COPY ./requirements.txt .
RUN pip install -r requirements.txt