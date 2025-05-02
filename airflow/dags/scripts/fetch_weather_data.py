import requests
import json
from datetime import datetime
import os


def fetch_weather(api_key, city="Toronto"):
    """OpenWeather API에서 실시간 날씨 데이터를 가져오는 함수"""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    # 필요한 데이터만 추출
    weather_info = {
        "timestamp": datetime.utcnow().isoformat(),
        "city": city,
        "temperature_celsius": data['main']['temp'],
        "humidity": data['main']['humidity'],
        "weather_description": data['weather'][0]['description']
    }
    return weather_info


if __name__ == "__main__":
    # 1. API Key 설정
    API_KEY = "4dd840884169a60780996e7a320a5ca5"

    # 2. 데이터 가져오기
    weather_data = fetch_weather(API_KEY, city="Toronto")

    # 3. 저장할 디렉토리 확인 및 생성
    output_dir = "data/raw"
    os.makedirs(output_dir, exist_ok=True)

    # 4. 파일명 만들기
    today = datetime.now().strftime("%Y%m%d")
    filename = f"{output_dir}/weather_{today}.json"

    # 5. JSON 파일로 저장
    with open(filename, "w") as f:
        json.dump(weather_data, f, indent=4)

    print(f"Saved weather data to {filename}")