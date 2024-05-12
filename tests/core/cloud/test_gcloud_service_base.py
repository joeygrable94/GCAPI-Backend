import pytest  # noqa: F401

from app.core.cloud.google import GDRIVE_SCOPES, GoCloudServiceType
from app.core.cloud.google.gcloud_access import (
    load_gcloud_credentials,
    load_gcloud_service,
)
from app.core.config import settings


def test_gcloud_load_gcloud_credentials() -> None:
    creds = load_gcloud_credentials(
        account=settings.cloud.googlecloudserviceaccount,
        scopes=GDRIVE_SCOPES,
    )
    assert creds is not None
    resource = load_gcloud_service(creds, GoCloudServiceType.drive)
    assert resource is not None
    resource.close()
