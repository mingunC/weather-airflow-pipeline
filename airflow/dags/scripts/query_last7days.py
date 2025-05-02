import pandas as pd
from google.cloud import bigquery
from datetime import datetime, timedelta

def query_last_7_days(project_id, dataset_id, table_id):
    client = bigquery.Client(project=project_id)
    table = f"`{project_id}.{dataset_id}.{table_id}`"

    # 지난 7일(오늘 포함) 일별 평균 기온
    sql = f"""
    SELECT
      DATE(timestamp) AS date,
      AVG(temperature_celsius) AS avg_temp_c
    FROM {table}
    WHERE DATE(timestamp) BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 6 DAY) AND CURRENT_DATE()
    GROUP BY date
    ORDER BY date
    """

    df = client.query(sql).to_dataframe()
    print(df)  # 콘솔 출력
    # CSV로 저장
    output_file = f"data/processed/last7days_{datetime.now():%Y%m%d}.csv"
    df.to_csv(output_file, index=False)
    print(f"Saved CSV to {output_file}")

if __name__ == "__main__":
    PROJECT_ID = "future-cat-458304-j8"
    DATASET_ID = "weather_data"
    TABLE_ID   = "weather_20250429"

    query_last_7_days(PROJECT_ID, DATASET_ID, TABLE_ID)