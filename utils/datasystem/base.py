import os

from io import StringIO, BytesIO
from typing import List, Iterator, Union

from minio import Minio
from minio.datatypes import Bucket, Object
import pandas
from pandas import DataFrame, Series


class DataSystem:
    """
    Class to work with local Minio data system
    """

    def __init__(self):

        self.client = Minio(
            "minio:9000",
            access_key=os.environ["minio_access_key"],
            secret_key=os.environ["minio_secret_key"],
            secure=False,
        )

    def list_buckets(self) -> List[Bucket]:
        """
        List all the buckets present within the Minio instance
        """
        buckets = self.client.list_buckets()
        return buckets

    def list_objects(self, bucket_name: str, prefix: str) -> Iterator[Object]:
        """
        List all of the objects present within a specificed Bucket
        and a given prefix
        """
        objects = self.client.list_objects(bucket_name, prefix)
        return objects

    def get_object(
        self, bucket_name: str, object_name: str, **kwargs
    ) -> Union[DataFrame, Series]:
        """
        Load a file from Minio storage to a pandas DataFrame
        """
        result = self.client.get_object(bucket_name, object_name)
        extension = object_name.split(".")[-1]
        try:
            status_code = result.status
            assert status_code == 200

            data = BytesIO()
            data.write(result.read())
            data.seek(0)

            if extension == "csv":
                return pandas.read_csv(data, **kwargs)

        except (Exception):
            raise InvalidObjectResponse

    def put_object(self, bucket_name: str, object_name: str, df: DataFrame) -> str:
        """
        Uploads a dataframe object to the Minio storage.

        Returns a string of the new object_name
        """
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        res = self.client.put_object(bucket_name, object_name, csv_buffer)
        return res.object_name
