import os

from azure.storage.blob import BlobServiceClient


def get_blob_client():
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.getenv("AZURE_STORAGE_CONTAINER", "sistemaprospect")
    blob_service = BlobServiceClient.from_connection_string(connection_string)
    return blob_service.get_container_client(container_name)


def upload_blob(filename: str, data: bytes, content_type: str = "application/json") -> str:
    container = get_blob_client()
    blob = container.get_blob_client(filename)
    blob.upload_blob(data, overwrite=True, content_settings={"content_type": content_type})
    return blob.url


def download_blob(filename: str) -> bytes:
    container = get_blob_client()
    blob = container.get_blob_client(filename)
    return blob.download_blob().readall()
