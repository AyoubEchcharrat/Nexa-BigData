from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="velib_api_ingestion",
    description="Ingestion des données Velib depuis l'API OpenData Paris",
    start_date=datetime(2025, 1, 1),
    schedule="30 * * * *",
    catchup=False,
    tags=["velib", "api"],
) as dag:

    fetch_velib_api = BashOperator(
        task_id="fetch_velib_api",
        bash_command="python /opt/airflow/projetBIGDATA/scripts/getapi.py",
    )
