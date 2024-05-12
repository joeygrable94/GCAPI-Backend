import os

from tests.utils.utils import get_tests_root_directory

from app.core.cloud.google import (
    GoCloudDriveAsset,
    GoCloudDriveAssetId,
    GoCloudDriveAssetsPage,
    GoCloudDriveService,
    GoCloudDriveSharedAsset,
)
from app.core.config import settings


def test_gdrive_list_paginated_files_and_folders() -> None:
    service = GoCloudDriveService(
        root_folder_id=settings.cloud.gocloud_gdrive_root_folder_id,
        public_folder_id=settings.cloud.gocloud_gdrive_public_folder_id,
        service_account=settings.cloud.googlecloudserviceaccount,
    )
    assets: GoCloudDriveAssetsPage = service.list_paginated(
        parent_id=settings.cloud.gocloud_gdrive_root_folder_id, files=True, folders=True
    )
    assert assets is not None
    assert assets.success is True
    assert assets.results is not None
    assert len(assets.results) >= 0
    assert not len(assets.results) > 10


def test_gdrive_list_paginated_files() -> None:
    service = GoCloudDriveService(
        root_folder_id=settings.cloud.gocloud_gdrive_root_folder_id,
        public_folder_id=settings.cloud.gocloud_gdrive_public_folder_id,
        service_account=settings.cloud.googlecloudserviceaccount,
    )
    files: GoCloudDriveAssetsPage = service.list_paginated()
    assert files is not None
    assert files.success is True
    assert files.results is not None
    assert len(files.results) >= 0
    assert not len(files.results) > 10
    files_2: GoCloudDriveAssetsPage = service.list_paginated(
        parent_id=settings.cloud.gocloud_gdrive_root_folder_id
    )
    assert files_2 is not None
    assert files_2.success is True
    assert files_2.results is not None
    assert len(files_2.results) >= 0
    assert not len(files_2.results) > 10


def test_gdrive_list_paginated_folders() -> None:
    service = GoCloudDriveService(
        root_folder_id=settings.cloud.gocloud_gdrive_root_folder_id,
        public_folder_id=settings.cloud.gocloud_gdrive_public_folder_id,
        service_account=settings.cloud.googlecloudserviceaccount,
    )
    folders: GoCloudDriveAssetsPage = service.list_paginated(
        size=10,
        parent_id=settings.cloud.gocloud_gdrive_root_folder_id,
        files=False,
        folders=True,
    )
    assert folders is not None
    assert folders.success is True
    assert folders.results is not None
    assert len(folders.results) >= 0
    assert not len(folders.results) > 10


def test_gdrive_create_file_and_read_file_by_id() -> None:
    service = GoCloudDriveService(
        root_folder_id=settings.cloud.gocloud_gdrive_root_folder_id,
        public_folder_id=settings.cloud.gocloud_gdrive_public_folder_id,
        service_account=settings.cloud.googlecloudserviceaccount,
    )
    root_dir = get_tests_root_directory()
    file_name = "test_csv_upload.csv"
    file_mime_type = "text/csv"
    test_csv_upload = f"{root_dir}/data/{file_name}"
    file_id: str = ""
    if os.path.isfile(test_csv_upload):
        uploaded_file = service.create(test_csv_upload)
        assert uploaded_file.success is True
        assert uploaded_file.asset_id is not None
        file_id = uploaded_file.asset_id
    file_by_id = service.read_file_by_id(file_id)
    assert file_by_id.success is True
    assert file_by_id.asset is not None
    assert file_by_id.asset.get("kind", "") == "drive#file"
    assert file_by_id.asset.get("id", "") == file_id
    assert file_by_id.asset.get("name", "") == file_name
    assert file_by_id.asset.get("mimeType", "") == file_mime_type


def test_gdrive_create_file_and_delete_file_move_to_trash() -> None:
    service = GoCloudDriveService(
        root_folder_id=settings.cloud.gocloud_gdrive_root_folder_id,
        public_folder_id=settings.cloud.gocloud_gdrive_public_folder_id,
        service_account=settings.cloud.googlecloudserviceaccount,
    )
    root_dir = get_tests_root_directory()
    file_name = "test_csv_upload.csv"
    test_csv_upload = f"{root_dir}/data/{file_name}"
    file_id: str = ""
    if os.path.isfile(test_csv_upload):
        uploaded_file = service.create(test_csv_upload)
        assert uploaded_file.success is True
        assert uploaded_file.asset_id is not None
        file_id = uploaded_file.asset_id
        deleted_file = service.delete(file_id)
        assert deleted_file.success is True
        assert deleted_file.asset_id == file_id


def test_gdrive_create_file_to_folder_id_and_read_file_by_id() -> None:
    service = GoCloudDriveService(
        root_folder_id=settings.cloud.gocloud_gdrive_root_folder_id,
        public_folder_id=settings.cloud.gocloud_gdrive_public_folder_id,
        service_account=settings.cloud.googlecloudserviceaccount,
    )
    root_dir = get_tests_root_directory()
    file_name = "test_csv_upload.csv"
    file_mime_type = "text/csv"
    test_csv_upload = f"{root_dir}/data/{file_name}"
    file_id: str = ""
    if os.path.isfile(test_csv_upload):
        uploaded_file = service.create(
            test_csv_upload, parent_id=settings.cloud.gocloud_gdrive_public_folder_id
        )
        assert uploaded_file.success is True
        assert uploaded_file.asset_id is not None
        file_id = uploaded_file.asset_id
    file_by_id = service.read_file_by_id(file_id)
    assert file_by_id.success is True
    assert file_by_id.asset is not None
    assert file_by_id.asset.get("kind", "") == "drive#file"
    assert file_by_id.asset.get("id", "") == file_id
    assert file_by_id.asset.get("name", "") == file_name
    assert file_by_id.asset.get("mimeType", "") == file_mime_type


def test_gdrive_update_file_by_id() -> None:
    service = GoCloudDriveService(
        root_folder_id=settings.cloud.gocloud_gdrive_root_folder_id,
        public_folder_id=settings.cloud.gocloud_gdrive_public_folder_id,
        service_account=settings.cloud.googlecloudserviceaccount,
    )
    root_dir = get_tests_root_directory()
    file_name = "test_csv_upload.csv"
    file_mime_type = "text/csv"
    test_csv_upload = f"{root_dir}/data/{file_name}"
    file_id: str = ""
    if os.path.isfile(test_csv_upload):
        uploaded_file = service.create(
            test_csv_upload, parent_id=settings.cloud.gocloud_gdrive_public_folder_id
        )
        assert uploaded_file.success is True
        assert uploaded_file.asset_id is not None
        file_id = uploaded_file.asset_id
    updated_file_by_id = service.update_file_by_id(
        file_id, file_path=test_csv_upload, file_name="updated_test_csv_upload.csv"
    )
    assert updated_file_by_id.success is True
    assert updated_file_by_id.asset_id is not None
    file_by_id: GoCloudDriveAsset = service.read_file_by_id(file_id)
    assert file_by_id.asset is not None
    assert file_by_id.asset.get("kind", "") == "drive#file"
    assert file_by_id.asset.get("id", "") == file_id
    assert file_by_id.asset.get("name", "") == "updated_test_csv_upload.csv"
    assert file_by_id.asset.get("mimeType", "") == file_mime_type
    delete_file = service.delete(file_id, skip_trash=True)
    assert delete_file.success is True
    assert delete_file.asset_id == file_id


def test_gdrive_update_file_by_id_file_not_exists() -> None:
    service = GoCloudDriveService(
        root_folder_id=settings.cloud.gocloud_gdrive_root_folder_id,
        public_folder_id=settings.cloud.gocloud_gdrive_public_folder_id,
        service_account=settings.cloud.googlecloudserviceaccount,
    )
    root_dir = get_tests_root_directory()
    file_name = "test_csv_upload.csv"
    test_csv_upload = f"{root_dir}/data/{file_name}"
    file_id: str = "unknown-id-1235198"
    updated_file_by_id = service.update_file_by_id(
        file_id, file_path=test_csv_upload, file_name="updated_test_csv_upload.csv"
    )
    assert updated_file_by_id.success is False
    assert updated_file_by_id.asset_id is None


def test_gdrive_create_folder_and_delete_folder_by_id() -> None:
    service = GoCloudDriveService(
        root_folder_id=settings.cloud.gocloud_gdrive_root_folder_id,
        public_folder_id=settings.cloud.gocloud_gdrive_public_folder_id,
        service_account=settings.cloud.googlecloudserviceaccount,
    )
    folder_name = "test_folder"
    new_folder: GoCloudDriveAssetId = service.create(folder_name, is_folder=True)
    assert new_folder.success is True
    assert new_folder.asset_id is not None
    deleted_folder = service.delete(
        new_folder.asset_id, is_folder=True, skip_trash=True
    )
    assert deleted_folder.success is True
    assert deleted_folder.asset_id == new_folder.asset_id


def test_gdrive_create_folder_and_list_by_name_files_then_folders() -> None:
    service = GoCloudDriveService(
        root_folder_id=settings.cloud.gocloud_gdrive_root_folder_id,
        public_folder_id=settings.cloud.gocloud_gdrive_public_folder_id,
        service_account=settings.cloud.googlecloudserviceaccount,
    )
    folder_name = "test_folder"
    new_folder: GoCloudDriveAssetId = service.create(folder_name, is_folder=True)
    assert new_folder.success is True
    assert new_folder.asset_id is not None
    new_sub_folder: GoCloudDriveAssetId = service.create(
        folder_name,
        parent_id=settings.cloud.gocloud_gdrive_public_folder_id,
        is_folder=True,
    )
    assert new_sub_folder.success is True
    assert new_sub_folder.asset_id is not None
    folders_by_name: GoCloudDriveAssetsPage = service.list_by_name(
        folder_name, files=False, folders=True
    )
    if folders_by_name.success and len(folders_by_name.results) > 0:
        for file in folders_by_name.results:
            assert file["name"] == folder_name
            deleted_file: GoCloudDriveAssetId = service.delete(
                file["id"], skip_trash=True
            )
            assert deleted_file.success is True
            assert deleted_file.asset_id == file["id"]


def test_gdrive_list_by_name_files() -> None:
    service = GoCloudDriveService(
        root_folder_id=settings.cloud.gocloud_gdrive_root_folder_id,
        public_folder_id=settings.cloud.gocloud_gdrive_public_folder_id,
        service_account=settings.cloud.googlecloudserviceaccount,
    )
    file_name = "test_csv_upload.csv"
    files_by_name: GoCloudDriveAssetsPage = service.list_by_name(file_name)
    if files_by_name.success and len(files_by_name.results) > 0:
        for file in files_by_name.results:
            assert file["name"] == file_name


def test_gdrive_list_by_name_files_and_folders() -> None:
    service = GoCloudDriveService(
        root_folder_id=settings.cloud.gocloud_gdrive_root_folder_id,
        public_folder_id=settings.cloud.gocloud_gdrive_public_folder_id,
        service_account=settings.cloud.googlecloudserviceaccount,
    )
    folder_name = "test_csv_upload"
    new_folder_uploaded, new_folder = service.create(  # noqa: F841
        folder_name, is_folder=True
    )
    find_assets_named = "test_csv_upload"
    assets_by_name: GoCloudDriveAssetsPage = service.list_by_name(
        find_assets_named, files=True, folders=True
    )
    if assets_by_name.success and len(assets_by_name.results) > 0:
        for asset in assets_by_name.results:
            assert find_assets_named in asset["name"]
            deleted_asset: GoCloudDriveAssetId = service.delete(
                asset["id"], skip_trash=True
            )
            assert deleted_asset.success is True
            assert deleted_asset.asset_id == asset["id"]


def test_gdrive_list_by_name_files_none_found() -> None:
    service = GoCloudDriveService(
        root_folder_id=settings.cloud.gocloud_gdrive_root_folder_id,
        public_folder_id=settings.cloud.gocloud_gdrive_public_folder_id,
        service_account=settings.cloud.googlecloudserviceaccount,
    )
    file_name = "test_csv_upload.csv"
    files_by_name = service.list_by_name(file_name)
    assert files_by_name.success is True
    assert files_by_name.results is not None
    assert len(files_by_name.results) == 0


def test_gdrive_share_file_with_email() -> None:
    service = GoCloudDriveService(
        root_folder_id=settings.cloud.gocloud_gdrive_root_folder_id,
        public_folder_id=settings.cloud.gocloud_gdrive_public_folder_id,
        service_account=settings.cloud.googlecloudserviceaccount,
    )
    test_file: dict = {}
    test_file_name = "test.txt"
    test_share_email = settings.auth.first_admin
    files: GoCloudDriveAssetsPage = service.list_by_name(test_file_name)
    assert files.success is True
    assert files.results is not None
    if files.success and len(files.results) > 0:
        test_file = files.results[0]
    assert test_file["name"] == test_file_name
    shared_data: GoCloudDriveSharedAsset
    shared_data = service.share_file_with_email(test_file["id"], test_share_email)
    assert shared_data is not None
    assert shared_data.success is True
    assert shared_data.request_id is not None
    assert shared_data.asset_id == test_file["id"]
    assert shared_data.email == settings.auth.first_admin
