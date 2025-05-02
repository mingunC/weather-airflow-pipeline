from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'ryan',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='weather_pipeline',
    default_args=default_args,
    description='Daily weather ETL & report pipeline',
    schedule_interval='0 6 * * *',
    start_date=datetime(2025, 5, 3),
    catchup=False,
) as dag:

    t1_fetch = BashOperator(
        task_id='fetch_weather',
        bash_command='python3 /opt/airflow/dags/scripts/fetch_weather_data.py'
    )

    t2_transform = BashOperator(
        task_id='transform_weather',
        bash_command='python3 /opt/airflow/dags/scripts/transform_weather_data.py'
    )

    t3_upload = BashOperator(
        task_id='upload_to_gcs',
        bash_command='python3 /opt/airflow/dags/scripts/upload_to_gcs.py'
    )

    t4_load = BashOperator(
        task_id='load_into_bq',
        bash_command='python3 /opt/airflow/dags/scripts/load_data_to_bigquery.py'
    )

    t5_report = BashOperator(
        task_id='generate_report',
        bash_command='python3 /opt/airflow/dags/scripts/query_last7days.py'
    )

    t1_fetch >> t2_transform >> t3_upload >> t4_load >> t5_report