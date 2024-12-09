from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os


class AzureBlobUploader:
    def __init__(self, container_url: str, token: str, container_name: str):
        # Container URL, Token, and Container Name are provided as parameters
        self.container_url = container_url
        self.token = token
        self.container_name = container_name  # Store the container name
        self.blob_service_client = BlobServiceClient(
            account_url=self.container_url, credential=self.token
        )
        self.container_client = self.blob_service_client.get_container_client(
            self.container_name
        )  # Pass the container name here

    def upload_file(self, file, file_name: str):
        """
        Upload a file to Azure Blob Storage.
        :param file: The file to upload (File object).
        :param file_name: The name for the file to be stored in the blob.
        :return: URL of the uploaded file.
        """
        blob_client = self.container_client.get_blob_client(file_name)

        try:
            blob_client.upload_blob(
                file, overwrite=True
            )  # Overwrite if file already exists
            print(f"File uploaded successfully: {file_name}")
            return blob_client.url  # Return the URL to the uploaded file
        except Exception as e:
            print(f"Error uploading file {file_name}: {e}")
            return None

    def upload_multiple_files(self, files):
        """
        Upload multiple files to the Blob Storage.
        :param files: List of file objects.
        :return: List of URLs to the uploaded files.
        """
        uploaded_urls = []
        for media_file in files:
            file_name = media_file.name  # Use the original file name
            file_url = self.upload_file(media_file, file_name)
            if file_url:
                uploaded_urls.append(file_url)
        return uploaded_urls
