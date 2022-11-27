FROM apache/airflow:2.3.0
USER airflow

COPY ./requirements.txt .

RUN python3 -m pip install --user --upgrade pip
RUN python3 -m pip install --no-cache-dir --user -r requirements.txt