import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
import streamlit as st

load_dotenv()

AZURE_STOREAGE_CONNECTION_STRING = os.getenv("AZURE_STOREAGE_CONNECTION_STRING")
AZURE_STOREAGE_CONTAINER_NAME = os.getenv("AZURE_STOREAGE_CONTAINER_NAME")

blob_service_client = BlobServiceClient.from_connection_string(AZURE_STOREAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(AZURE_STOREAGE_CONTAINER_NAME)


def upload_file_to_azure(file_path, blob_name):
    # blob_name 으로 파일 업로드
    try:
        with open(file_path, "rb") as data:
            container_client.upload_blob(name=blob_name, data=data)
        print(f"File {file_path} uploaded to Azure Blob Storage as {blob_name}.")
    except Exception as e:
        print(f"Error uploading file to Azure Blob Storage: {e}")

def download_file_from_azure(blob_name, download_path):
    # blob_name인 파일 다운로드
    try:
        with open(download_path, "wb") as download_file:
            download_stream = container_client.download_blob(blob_name)
            download_file.write(download_stream.readall())
        print(f"File {blob_name} downloaded from Azure Blob Storage to {download_path}.")
    except Exception as e:
        print(f"Error downloading file from Azure Blob Storage: {e}")

def delete_file_from_azure(blob_name):
    # blob_name인 파일 삭제
    try:
        container_client.delete_blob(blob_name)
        print(f"File {blob_name} deleted from Azure Blob Storage.")
    except Exception as e:
        print(f"Error deleting file from Azure Blob Storage: {e}")

def list_files_in_azure():
    # 컨테이너 내 모든 파일 리스트 출력
    try:
        blob_list = container_client.list_blobs()
        print("Files in Azure Blob Storage:")
        for blob in blob_list:
            print(f"- {blob.name}")
    except Exception as e:
        print(f"Error listing files in Azure Blob Storage: {e}")



if __name__ == "__main__":

    st.title("Azure Blob Storage 파일 업로드")
    uploaded_file = st.file_uploader("파일 선택", type=["txt", "csv", "png", "jpg", "jpeg"])

    if uploaded_file is not None:
        file_name, file_extension = os.path.splitext(uploaded_file.name)

        # 파일을 임시로 저장
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"파일 {uploaded_file.name} 업로드 완료")

        # Azure에 파일 업로드
        upload_file_to_azure(uploaded_file.name, f"{file_name}-uploaded{file_extension}")
        st.success(f"파일 {uploaded_file.name} Azure Blob Storage에 업로드 완료")

        # 업로드된 파일 리스트 출력
        st.subheader("Azure Blob Storage 파일 리스트")
        blob_list = container_client.list_blobs()
        for blob in blob_list:
            st.write(f"- {blob.name}")
