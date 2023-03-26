from prefect.filesystems import RemoteFileSystem

base_settings = {
    "key": "minio_admin",
    "secret": "minio_password",
    "client_kwargs": {"endpoint_url": "http://localhost:9000"},
}

# Create the file system connection for the remote bucket
RemoteFileSystem(
    basepath="s3://raw-data",
    settings=base_settings,
).save("raw-s3")

# Create the file system connection for the processed bucket
RemoteFileSystem(basepath="s3://processed-data", settings=base_settings).save(
    "processed-s3"
)

# Create the file system connection for the enriched bucket
RemoteFileSystem(basepath="s3://enriched-data", settings=base_settings).save(
    "enriched-s3"
)
