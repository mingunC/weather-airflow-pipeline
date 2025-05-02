from google.cloud import storage
import os
from datetime import datetime

def upload_to_gcs(bucket_name, source_file_path, destination_blob_name):
    """Local 파일을 GCP Storage로 업로드하는 함수"""
    storage_client = storage.Client()
    bucket = storage_client.bucket("weather-data-bucket-cmgg919")
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_path)
    print(f"Uploaded {source_file_path} to gs://{bucket_name}/{destination_blob_name}")

if __name__ == "__main__":
    # 설정
    bucket_name = "weather-data-bucket-cmgg919"  # 네가 만든 버킷 이름
    today = datetime.now().strftime("%Y%m%d")
    # source_file = f"data/raw/weather_{today}.json"
    # destination_blob = f"weather_data/weather_{today}.json"
    # 예시: upload_to_gcs.py 수정
    source_file = "data/processed/processed_weather_20250429_ld.json"
    destination_blob = "weather_data/processed_weather_20250429_ld.json"

    upload_to_gcs(bucket_name, source_file, destination_blob)
