import requests
from prefect import flow, task
from prefect.filesystems import RemoteFileSystem

files_raw = RemoteFileSystem.load("raw-s3")


@task
def call_api(url):
    response = requests.get(url)
    print(response.status_code)
    return response.json()


@task
def parse_fact(response):
    fact = response["fact"]
    print(fact)
    return fact


@flow(
    name="Example flow",
    description="This is just an example flow that prefect can run, contains two tasks and saves a raw text file to Minio",
    log_prints=True,
)
def api_flow(url):
    fact_json = call_api(url)
    fact_text = parse_fact(fact_json)
    files_raw.write_path("/test.txt", fact_text.encode("utf-8"))


api_flow("https://catfact.ninja/fact")
