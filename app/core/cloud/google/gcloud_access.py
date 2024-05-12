from typing import Any, Dict

from google.oauth2 import service_account
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from .gcloud_schemas import GoCloudServiceType, GoCloudServiceVersion


def load_gcloud_credentials(account: Dict[str, Any], scopes: list[str]) -> Credentials:
    credentials: Credentials = service_account.Credentials.from_service_account_info(
        info=account,
        scopes=scopes,
    )
    return credentials


def load_gcloud_service(
    credentials: Credentials,
    service: GoCloudServiceType,
) -> Any:
    service_version = GoCloudServiceVersion[service.value]
    source = build(
        service.value,
        version=service_version.value,
        credentials=credentials,
    )
    return source
