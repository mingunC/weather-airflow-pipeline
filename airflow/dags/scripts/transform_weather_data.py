import pandas as pd
import json
import os
from datetime import datetime

def load_weather_json(file_path):
    """Json 파일을 읽어 Data frame으로 변화"""
    with open(file_path, "r") as f:
        data = json.load(f)
    df = pd.DataFrame([data])
    return df

def clean_weather_data(df):
    """데이터 클렌징 작업"""
    #결측치 처리
    df['temperature_celsius'] = df['temperature_celsius'].fillna(-999)
    df['humidity'] = df['humidity'].fillna(-1)

    #timestamp를 datatime 타입으로 변환
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    #weather_description 컬럼 소문자로 변환
    df['weather_description'] = df['weather_description'].str.lower()
    return df

def save_weather_data(df, output_path):
    """
    newline-delimited JSON 으로 저장
    """
    # orient="records", lines=True 로 각 레코드를 한 줄에 하나씩 저장
    df.to_json(output_path, orient="records", date_format="iso", lines=True)


if __name__ == "__main__":
    today = "20250429"
    input_file = f"./data/raw/weather_20250429.json"
    output_file = f"data/processed/processed_weather_{today}_ld.json"
    # 디렉토리 확인
    os.makedirs('data/processed', exist_ok=True)
    # 데이터 로드
    df = load_weather_json(input_file)
    # 데이터 클렌징
    df = clean_weather_data(df)
    # 결과 저장
    save_weather_data(df, output_file)

    print(f"Saved newline-delimited JSON to {output_file}")