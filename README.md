# Local Datalake

Simple Docker & Python project to run local data pipelines on. The idea is to have a single repo running locally that can mock cloud data storage and can mock programmatic data pipelines.

## Project Architecture

The project can be run using a single `docker-compose` command, made up of the following:

1. Minio - This a high performance object storage. It is API compatible with AWS S3 and we use it as a mocker.
2. Prefect - A open source Python dataflow automation tool. We use this to write our core data pipelines.
3. Postgres - Used for a metadata engine for Prefect but also for the ability to write to a SQL data warehouse.

## Getting Started [MacOS]

Currently support for MacOS which is what I develop on. Should port quite easy to others if required.

To get started install the required packages using `brew`.

```
make brew
```

Install the required Python system.

```
make python-setup
```

Copy over the `.env.example` to a `.env` file and populate the required variables. Then fire up the docker compose and get all the systems running.

```
make setup
make setup/buckets
```

The second command creates three buckets on Minio. This follows the typical data engineering pattern of a `raw-data` bucket where all initial data should be placed. Once processed using some initial pipeline place this data in `processed-data` and finally any collections of features should be placed in the `enriched-bucket`. There is a choice here on whether this gets saved to the SQL warehouse.

Once everything is setup and running you should be able to browse to `http://localhost:9000` to see the Minio admin console. Login in using `minio_admin` and `minio_password` to see the three buckets ready to accept data.

## Data Pipelines

We use Prefect to run our dataflows. First setup up the virtual environment `make venv`. Prefect has a useful built in file system that we can connect to Minio to read and write data too. To setup the Prefect minio connection run `python utils/filesystem.py`.

To run a Prefect workflow just simply run the Python file directly `python pipeline/example/main.py`.
