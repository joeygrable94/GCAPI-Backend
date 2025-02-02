# Cloud Storage

This package was modifed from the original source to fit the needs of the project.

## Source Code Acknowledgement

- [fastapi-cloud-drives](https://github.com/AliyevH/fastapi-cloud-drives)
- Credit to [@AliyevH](https://github.com/AliyevH) on GitHub or via [GMail](hasan.aliyev.555@gmail.com) for the original package.

## Examples

### AWS S3

```python
from logging import debug

from botocore.serialize import JSONSerializer
from app.core.storage import S3Storage

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

s3_client = S3Storage(default_region="us-west-2", default_bucket="fastapibucket")


@app.get("/list_buckets")
async def list_buckets():
    buckets = await s3_client.list_buckets()
    return JSONResponse(status_code=200, content=buckets)

@app.get("/create_bucket")
async def create_bucket():
    created = await s3_client.create_bucket(bucket_name="fastapibucket")
    return JSONResponse(status_code=200, content=created)

@app.get("/upload_file")
async def upload_file():
    created = await s3_client.upload_file(
        bucket_name="fastapibucket",
        file_name="fastapi.txt",
        object_name="fastapi.txt"
        )
    return JSONResponse(status_code=200, content=created)

@app.get("/download_file")
async def download_file():
    f = await s3_client.download_file(
        bucket_name="fastapibucket",
        file_name="fastapi.txt",
        object_name="fastapi.txt"
        )
    return JSONResponse(status_code=200, content=f)

@app.get("/list_objects")
async def list_objects():
    page_iterator = await s3_client.list_objects(bucket_name="fastapibucket")
    for page in page_iterator:
        print(page.get("Contents"))
    return JSONResponse(status_code=200)
```
