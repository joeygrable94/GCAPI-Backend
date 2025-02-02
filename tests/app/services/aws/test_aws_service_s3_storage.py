import pytest
from boto3 import Session

from app.services.aws import S3Storage
from app.services.aws.settings import aws_settings
from tests.utils.utils import get_tests_root_directory

pytestmark = pytest.mark.asyncio


async def test_s3_storage_service_list_objects() -> None:
    s3 = S3Storage(
        default_region=aws_settings.aws_default_region,
        default_bucket=aws_settings.aws_s3_default_bucket,
    )
    bucket_name = aws_settings.aws_s3_default_bucket
    assert s3.region == aws_settings.aws_default_region
    assert isinstance(s3.session, Session)
    assert s3.s3_client is not None
    public_objs = s3.list_objects(
        prefix="public/",
        bucket_name=bucket_name,
    )
    for page in public_objs:
        assert len(page["Contents"]) >= 1
        assert page["Prefix"] == "public/"
    root_objs = s3.list_objects(
        bucket_name=bucket_name,
    )
    for page in root_objs:
        assert len(page["Contents"]) >= 1
        assert page["Prefix"] == ""
    root_objs_no_bucket_provided = s3.list_objects()
    for page in root_objs_no_bucket_provided:
        assert len(page["Contents"]) >= 1
        assert page["Prefix"] == ""


async def test_s3_storage_service_file_exists() -> None:
    s3 = S3Storage(
        default_region=aws_settings.aws_default_region,
        default_bucket=aws_settings.aws_s3_default_bucket,
    )
    bucket_name = aws_settings.aws_s3_default_bucket
    object_name = "test.txt"
    content: bool = s3.file_exists(
        object_name=object_name,
        bucket_name=bucket_name,
    )
    assert content is True


async def test_s3_storage_service_file_exists_not_found() -> None:
    s3 = S3Storage(
        default_region=aws_settings.aws_default_region,
        default_bucket=aws_settings.aws_s3_default_bucket,
    )
    bucket_name = aws_settings.aws_s3_default_bucket
    object_name = "test-not-found.txt"
    content: bool = s3.file_exists(
        object_name=object_name,
        bucket_name=bucket_name,
    )
    assert content is False


async def test_s3_storage_service_read_file_contents_not_found() -> None:
    s3 = S3Storage(
        default_region=aws_settings.aws_default_region,
        default_bucket=aws_settings.aws_s3_default_bucket,
    )
    bucket_name = aws_settings.aws_s3_default_bucket
    object_name = "test-not-found.txt"
    content: str | None = s3.read_file_content(
        object_name=object_name,
        bucket_name=bucket_name,
    )
    assert content is None


async def test_s3_storage_service_upload_file_read_file_contents() -> None:
    s3 = S3Storage(
        default_region=aws_settings.aws_default_region,
        default_bucket=aws_settings.aws_s3_default_bucket,
    )
    bucket_name = aws_settings.aws_s3_default_bucket
    object_name = "test.txt"
    test_root_dir = get_tests_root_directory()
    file_name = f"{test_root_dir}/data/{object_name}"
    uploaded = s3.upload_file(
        file_path=file_name,
        object_name=object_name,
        bucket_name=bucket_name,
    )
    assert uploaded is True
    content: str | None = s3.read_file_content(
        object_name=object_name,
        bucket_name=bucket_name,
    )
    assert content == "Hello, World!"


async def test_s3_storage_service_upload_file_read_file_contents_no_obj_name() -> None:
    s3 = S3Storage(
        default_region=aws_settings.aws_default_region,
        default_bucket=aws_settings.aws_s3_default_bucket,
    )
    bucket_name = aws_settings.aws_s3_default_bucket
    object_name = "test.txt"
    test_root_dir = get_tests_root_directory()
    file_name = f"{test_root_dir}/data/{object_name}"
    uploaded = s3.upload_file(
        file_path=file_name,
        bucket_name=bucket_name,
    )
    assert uploaded is True
    content: str | None = s3.read_file_content(
        object_name=object_name,
        bucket_name=bucket_name,
    )
    assert content == "Hello, World!"


async def test_s3_storage_service_download_file() -> None:
    s3 = S3Storage(
        default_region=aws_settings.aws_default_region,
        default_bucket=aws_settings.aws_s3_default_bucket,
    )
    bucket_name = aws_settings.aws_s3_default_bucket
    object_key = "test.txt"
    local_object_key = "test-downloaded.txt"
    test_root_dir = get_tests_root_directory()
    local_file_name = f"{test_root_dir}/data/{local_object_key}"
    downloaded = s3.download_file(
        file_path=local_file_name,
        object_key=object_key,
        bucket_name=bucket_name,
    )
    assert downloaded is True
    if downloaded:
        with open(local_file_name, "r") as file:
            content = file.read()
            assert content == "Hello, World!"


async def test_s3_storage_service_download_file_object_key_not_exists() -> None:
    s3 = S3Storage(
        default_region=aws_settings.aws_default_region,
        default_bucket=aws_settings.aws_s3_default_bucket,
    )
    bucket_name = aws_settings.aws_s3_default_bucket
    object_key = "test-not_found.txt"
    local_object_key = "test-download-fail.txt"
    test_root_dir = get_tests_root_directory()
    local_file_name = f"{test_root_dir}/data/{local_object_key}"
    downloaded = s3.download_file(
        file_path=local_file_name,
        object_key=object_key,
        bucket_name=bucket_name,
    )
    assert downloaded is False
