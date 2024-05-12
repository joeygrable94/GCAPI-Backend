# Example usage

    files = service.list_files_in_folder(parent_id=settings.cloud.gocloud_gdrive_root_folder_id)
    (True, [{'id': 'nabnShOsyXctcWsY1L9mpu5KK9mS7WncA', 'name': 'test.txt'}])

    folders = service.list_folders_in_folder(parent_id=settings.cloud.gocloud_gdrive_root_folder_id)
    (True, [{'id': 'MREFyI-TxeLncitLPZqO1LeFU_E6Lq9Qt', 'name': 'public'}])

    uploaded_file = service.upload_file(test_csv_upload)
    (True, {'id': 'LsjMP1FqLWE5ztkT35kjvjPowTo-QI2rH'})

    file_by_id = service.read_file_by_id(file["id"])
    (True, {'kind': 'drive#file', 'id': '1Li0mFlOAM8UOqwTk1WgeTGOOQfIeFSQE', 'name': 'test_csv_upload.csv', 'mimeType': 'text/csv'})

    files_by_name = service.find_files_by_name(file_name)
    (True, [
        {'id': '1FqLWkT35kjvjPowTo-E5ztLsjMPQI2rH', 'name': 'test_csv_upload.csv'},
        {'id': '10XI_LJNBaJ4mUsxdufd6XjC96m_6ccMc', 'name': 'test_csv_upload.csv'}
    ])

    deleted_file = service.delete_file(file["id"])
    (True, '1Li0mFlOAM8UOqwTk1WgeTGOOQfIeFSQE')

    folder = service.files().create(body=file_metadata, fields='id').execute()
    (True, {'id': '1M7zQ9ljSPscqQhNhYdY2J0k2Zz1Hoj1d'})

    folders_by_name = service.find_folders_by_name(folder_name)
    (True, [{'id': '1Xfa-5TSxrfyiRlQfe0ml9unmgocTrVpW', 'name': 'test_folder'}, {'id': '1hczjCHUig467u46KKgbrIZIzd1YPEUdB', 'name': 'test_folder'}])
