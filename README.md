# Local Datalake

Project to spin up a local datalake for local data engineering pipelines. It consists of data pipelines coded up in Python and orchestrated by Apache Airflow. A local version of AWS S3 (Minio) is used for data storage alongside a PostgreSQL database for data warehousing.

## Getting Started

### Infrastructure

```
make pre-setup
```

Setups the relevant Docker system.

```
make setup
```

Runs the core Docker compose file required to spin up all the services locally. Once all the services are running we create three default buckets within Minio, replicating a setup you would typically find in a production cloud setup. It then creates a Minio service account based on the admin, this service account is needed to generate the two API keys for the pipeline utils.