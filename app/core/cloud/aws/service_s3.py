import os
import sys
import threading
from pathlib import Path
from typing import Any, Iterator

from boto3 import Session, client
from botocore.exceptions import ClientError

from app.core.logger import logger


class S3Storage:
    def __init__(self, default_region: str, default_bucket: str):
        self.region: str = default_region
        self.session: Session = Session()
        self.s3_resource = self.session.resource("s3")
        self.s3_client = client("s3", self.region)
        self.default_bucket: str = default_bucket

    async def read_file_content(
        self, object_name: str, bucket_name: str | None = None
    ) -> str | None:
        """Read file content from S3.

        Args:
            object_name (str): Object name to read from.
            bucket_name (str, optional): Bucket name to read from.
                Defaults to default bucket.

        Returns:
            str | None: The content of file as string, None if error occurs.
        """
        try:
            from_bucket = self.default_bucket if bucket_name is None else bucket_name
            response = self.s3_client.get_object(Bucket=from_bucket, Key=object_name)
            return response["Body"].read().decode("utf-8")
        except ClientError as e:
            logger.exception(e)
            return None

    async def upload_file(
        self,
        file_path: str,
        object_name: str | None = None,
        bucket_name: str | None = None,
        extra_args: dict | None = None,
    ) -> bool:
        """Upload a file to an S3 bucket.

        Args:
            file_path (str): Path to file being uploaded to S3.
            object_name (str, optional): Defaults to the current filename.
            extra_args (dict, optional): Defaults to None.
            bucket_name (str, optional): Bucket to upload to.

        Returns:
            bool: True if upload was successful, False otherwise.
        """
        from_bucket = self.default_bucket if bucket_name is None else bucket_name
        __s3_bucket = self.s3_resource.Bucket(from_bucket)
        # If S3 object_name was not specified, use the name of the file_path provided
        object_name = Path(file_path).name if object_name is None else object_name
        # Upload the file
        try:
            __s3_bucket.upload_file(
                file_path,
                object_name,
                ExtraArgs=extra_args,
                Callback=ProgressPercentage(file_path),
            )
        except ClientError as e:  # pragma: no cover
            logger.exception(e)
            return False
        return True

    async def download_file(
        self,
        file_path: str,
        object_key: str,
        bucket_name: str | None = None,
        extra_args: dict | None = None,
    ) -> bool:
        """Download file from Bucket.

        Args:
            file_path (str): file_path is used to write bytes of object
                downloaded from bucket.
            object_key (str): The full object key located in bucket
                (prefix + object_name).
            bucket_name (str, optional): Name of bucket to download from.
                Defaults to default bucket.
            extra_args (dict, optional): [description]. Defaults to None.

        Returns:
            bool: True if download was successful, False otherwise.
        """
        from_bucket = self.default_bucket if bucket_name is None else bucket_name
        __s3_bucket = self.s3_resource.Bucket(from_bucket)
        try:
            # with open(file_path, "wb"):
            __s3_bucket.download_file(object_key, file_path, ExtraArgs=extra_args)
        except Exception as err:
            logger.exception(err)
            return False
        return True

    async def list_objects(
        self, prefix: str | None = None, bucket_name: str | None = None
    ) -> Iterator:
        """List objects in Bucket.

        Args:
            prefix (str, optional): Prefix parameter used to filter the
                paginated results by prefix server-side before sending them
                to the client. Defaults to None.
            bucket_name (str, optional): Name of Bucket. Defaults to default bucket.

        Returns:
            Iterator: PageIterator object.
        """
        from_bucket = self.default_bucket if bucket_name is None else bucket_name
        operation_parameters: Any = {"Bucket": from_bucket}
        if prefix:
            operation_parameters["Prefix"] = prefix
        paginator = self.s3_client.get_paginator("list_objects")
        page_iterator = paginator.paginate(**operation_parameters)
        return page_iterator

    '''
    async def list_buckets(self) -> list[str]:
        """[List existing buckets]

        Returns:
            [dict]: [List of buckets]
        """
        buckets = []
        for bucket in self.s3_resource.buckets.all():
            buckets.append(bucket.name)
        return buckets

    async def create_bucket(self, bucket_name: str) -> bool:
        """Create an S3 bucket in a specified region

        If a region is not specified, the bucket is created in the S3 default
        region (us-west-1).

        Args:
            bucket_name (str): [Bucket name to create bucket in s3]

        :param bucket_name: Bucket to create
        :param region: String region to create bucket in, e.g., 'us-west-1'
        :return: True if bucket created, else False
        """
        # Create bucket
        try:
            if self.region is None:
                self.s3_resource.create_bucket(Bucket=bucket_name)
            else:
                location = {"LocationConstraint": self.region}
                self.s3_resource.create_bucket(
                    Bucket=bucket_name, CreateBucketConfiguration=location
                )
        except ClientError as e:
            logger.exception(e)
            return False
        return True
    '''


class ProgressPercentage(object):
    def __init__(self, filename: str) -> None:
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount: Any) -> None:  # pragma: no cover
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)"
                % (self._filename, self._seen_so_far, self._size, percentage)
            )
            sys.stdout.flush()
