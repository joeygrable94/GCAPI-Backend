from __future__ import annotations

import os
from mimetypes import MimeTypes
from typing import TYPE_CHECKING, Any

from google.oauth2.service_account import Credentials
from googleapiclient.http import HttpError, MediaFileUpload
from pydantic import EmailStr

from app.core.logger import logger

from .constants import GDRIVE_SCOPES
from .gcloud_access import load_gcloud_credentials, load_gcloud_service
from .gcloud_schemas import (
    GoCloudDriveAsset,
    GoCloudDriveAssetId,
    GoCloudDriveAssetsPage,
    GoCloudDriveSharedAsset,
    GoCloudServiceType,
)

if TYPE_CHECKING:  # pragma: no cover
    from googleapiclient._apis.drive.v3 import DriveResource  # type: ignore
    from googleapiclient._apis.drive.v3 import FileList  # type: ignore


class GoCloudDriveService:
    root_folder_id: str
    public_folder_id: str
    service_account: dict
    delegated_account: str
    credentials: Credentials
    service: GoCloudServiceType
    scopes: list[str]

    def __init__(
        self,
        root_folder_id: str,
        public_folder_id: str,
        service_account: dict,
        service: GoCloudServiceType = GoCloudServiceType.drive,
        scopes: list[str] = GDRIVE_SCOPES,
    ):
        self.root_folder_id = root_folder_id
        self.public_folder_id = public_folder_id
        self.scopes = scopes
        self.service_account = service_account
        self.service = service
        self.credentials = load_gcloud_credentials(service_account, scopes)

    # LIST
    def list_paginated(
        self,
        size: int = 10,
        parent_id: str | None = None,
        files: bool = True,
        folders: bool = False,
        page_token: str | None = None,
    ) -> GoCloudDriveAssetsPage:
        parent_id = self.public_folder_id if parent_id is None else parent_id
        service: DriveResource = load_gcloud_service(self.credentials, self.service)
        success: bool = False
        items: list = []
        next_page_token: str | None = None
        query: str = ""
        error_message: str = ""
        if files and not folders:
            query = f"'{parent_id}' in parents and mimeType != 'application/vnd.google-apps.folder'"  # noqa: E501
            error_message = "Error listing files in Google Drive: "
        elif not files and folders:
            query = f"'{parent_id}' in parents and mimeType = 'application/vnd.google-apps.folder'"  # noqa: E501
            error_message = "Error listing folders in Google Drive: "
        else:
            query = f"'{parent_id}' in parents"
            error_message = "Error listing files and folders in Google Drive: "
        try:
            results: FileList
            if page_token:
                results = (
                    service.files()  # pragma: no cover
                    .list(
                        q=query,
                        pageSize=size,
                        pageToken=page_token,
                        fields="nextPageToken, files(id, name)",
                    )
                    .execute()
                )
            else:
                results = (
                    service.files()
                    .list(
                        q=query, pageSize=size, fields="nextPageToken, files(id, name)"
                    )
                    .execute()
                )
            items = results.get("files", [])
            next_page_token = results.get("nextPageToken", None)
            success = True
        except HttpError as error:  # pragma: no cover
            success = False
            logger.info(error_message, error.reason)
        except Exception as error:  # pragma: no cover
            success = False
            logger.info(error_message, error)
        finally:
            service.close()
            return GoCloudDriveAssetsPage(
                success=success,
                results=items,
                next_page_token=next_page_token,
            )

    def list_by_name(
        self,
        name: str,
        size: int = 10,
        files: bool = True,
        folders: bool = False,
        page_token: str | None = None,
    ) -> GoCloudDriveAssetsPage:
        service: DriveResource = load_gcloud_service(self.credentials, self.service)
        success: bool = False
        items: list = []
        next_page_token: str | None = None
        query: str = ""
        error_message: str = ""
        if not files and folders:
            query = f"name contains '{name}' and mimeType = 'application/vnd.google-apps.folder'"  # noqa: E501
            error_message = "Error retrieving matching folders from Google Drive: "
        elif files and not folders:
            query = f"name contains '{name}' and mimeType != 'application/vnd.google-apps.folder'"  # noqa: E501
            error_message = "Error retrieving matching files from Google Drive: "
        else:
            query = f"name contains '{name}'"
            error_message = (
                "Error retrieving matching files and folders from Google Drive: "
            )
        try:
            results: FileList
            if page_token:
                results = (
                    service.files()  # pragma: no cover
                    .list(
                        q=query,
                        pageSize=size,
                        pageToken=page_token,
                        fields="nextPageToken, files(id, name)",
                    )
                    .execute()
                )
            else:
                results = (
                    service.files()
                    .list(
                        q=query, pageSize=size, fields="nextPageToken, files(id, name)"
                    )
                    .execute()
                )
            items = results.get("files", [])
            next_page_token = results.get("nextPageToken", None)
            success = True
        except HttpError as error:  # pragma: no cover
            success = False
            logger.info(error_message, error.reason)
        except Exception as error:  # pragma: no cover
            success = False
            logger.info(error_message, error)
        finally:
            service.close()
            return GoCloudDriveAssetsPage(
                success=success,
                results=items,
                next_page_token=next_page_token,
            )

    # CREATE
    def create(
        self, name: str, parent_id: str | None = None, is_folder: bool = False
    ) -> GoCloudDriveAssetId:
        service: DriveResource = load_gcloud_service(self.credentials, self.service)
        success: bool = False
        asset_id: str | None = None
        error_message: str = ""
        if is_folder:
            error_message = "Error creating folder in Google Drive: "
        else:
            error_message = "Error creating file in Google Drive: "
        try:
            file_metadata: Any = {
                "name": os.path.basename(name),
            }
            if parent_id is not None:
                file_metadata["parents"] = [parent_id]
            else:
                file_metadata["parents"] = [self.root_folder_id]
            asset: dict
            if is_folder:
                file_metadata["mimeType"] = "application/vnd.google-apps.folder"
                asset = (
                    service.files().create(body=file_metadata, fields="id").execute()  # type: ignore  # noqa: E501
                )
            else:
                mime = MimeTypes()
                media = MediaFileUpload(
                    name,
                    mimetype=mime.guess_type(os.path.basename(name))[0],
                    resumable=True,
                )
                asset = (
                    service.files()  # type: ignore
                    .create(body=file_metadata, media_body=media, fields="id")
                    .execute()
                )
            asset_id = asset.get("id", None)
            success = True
        except HttpError as error:  # pragma: no cover
            success = False
            logger.info(error_message, error.reason)
        except Exception as error:  # pragma: no cover
            success = False
            logger.info(error_message, error)
        finally:
            service.close()
            return GoCloudDriveAssetId(success=success, asset_id=asset_id)

    # READ
    def read_file_by_id(self, file_id: str) -> GoCloudDriveAsset:
        service: DriveResource = load_gcloud_service(self.credentials, self.service)
        success: bool = False
        asset: dict | None = None
        error_message: str = "Error retrieving asset from Google Drive: "
        try:
            asset = service.files().get(fileId=file_id).execute()  # type: ignore
            success = True
        except HttpError as error:  # pragma: no cover
            success = False
            logger.info(error_message, error.reason)
        except Exception as error:  # pragma: no cover
            success = False
            logger.info(error_message, error)
        finally:
            service.close()
            return GoCloudDriveAsset(success=success, asset=asset)

    # UPDATE
    def update_file_by_id(
        self, file_id: str, file_path: str, file_name: str | None = None
    ) -> GoCloudDriveAssetId:
        service: DriveResource = load_gcloud_service(self.credentials, self.service)
        success: bool = False
        error_message: str = "Error updating asset in Google Drive: "
        asset_id: str | None = None
        try:
            file_exists, file_meta = self.read_file_by_id(file_id)
            if not file_exists:
                raise Exception(
                    "No asset found with file id provided"
                )  # pragma: no cover
            file_metadata: Any = {  # pragma: no cover
                "name": (
                    file_name if file_name is not None else os.path.basename(file_path)
                ),
            }
            mime = MimeTypes()
            media = MediaFileUpload(
                file_path,
                mimetype=mime.guess_type(os.path.basename(file_path))[0],
                resumable=True,
            )
            asset: dict = (
                service.files()  # type: ignore
                .update(fileId=file_id, body=file_metadata, media_body=media)
                .execute()
            )
            asset_id = asset.get("id", None)
            success = True
        except HttpError as error:  # pragma: no cover
            success = False
            logger.info(error_message, error.reason)
        except Exception as error:  # pragma: no cover
            success = False
            logger.info(error_message, error)
        finally:
            service.close()
            return GoCloudDriveAssetId(success=success, asset_id=asset_id)

    # DELETE
    def delete(
        self, asset_id: str, is_folder: bool = False, skip_trash: bool = False
    ) -> GoCloudDriveAssetId:
        """
        WARNING: using the is_folder flag will delete the folder and all its contents
        WARNING: using the skip_trash flag will permanently delete the assets
        """
        service: DriveResource = load_gcloud_service(self.credentials, self.service)
        success: bool = False
        error_message: str = ""
        if is_folder:
            error_message = "Error trashing folder and its contents from Google Drive: "
        else:
            error_message = "Error trashing file from Google Drive: "
        try:
            if skip_trash:
                service.files().delete(fileId=asset_id).execute()
            else:
                service.files().update(
                    fileId=asset_id, body={"trashed": True}
                ).execute()
            success = True
        except HttpError as error:  # pragma: no cover
            success = False
            logger.info(error_message, error.reason)
        finally:
            service.close()
            return GoCloudDriveAssetId(success=success, asset_id=asset_id)

    # SHARE
    def share_file_with_email(
        self, file_id: str, email: EmailStr
    ) -> GoCloudDriveSharedAsset:
        service: DriveResource = load_gcloud_service(self.credentials, self.service)
        success: bool = False
        request_id: str = ""
        try:
            user_permission: Any = {
                "type": "user",
                "role": "reader",
                "emailAddress": email,
            }
            results = (
                service.permissions()
                .create(fileId=file_id, body=user_permission, fields="id")
                .execute()
            )
            request_id = results.get("id", "")
            success = True
            logger.info(f"Shared file in Google Drive with email: {email}")
        except HttpError as error:  # pragma: no cover
            success = False
            logger.info("Error sharing file in Google Drive with email: ", error.reason)
        except Exception as error:  # pragma: no cover
            success = False
            logger.info("Error creating folder in Google Drive: ", error)
        finally:
            service.close()
            return GoCloudDriveSharedAsset(
                success=success, request_id=request_id, asset_id=file_id, email=email
            )
