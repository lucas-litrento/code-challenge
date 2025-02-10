from datetime import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
from update_data_path import update_data_path

from docker.types import Mount

default_args = {
    'owner': 'airflow',
    'depends_on_past': True,
    'retries': 1,
}

import os

path_airflow_folder = "/home/usuario/pasta_1/pasta_2/indicium_code_challenger/Airflow"

def meltano_task(task_id, mounts, entrypoint, dag):
    return DockerOperator(
        api_version='auto',
        dag=dag,
        task_id=task_id,
        image="meltano",
        entrypoint=entrypoint,
        auto_remove=True,
        mount_tmp_dir=False,
        network_mode='airflow_default',
        mounts=mounts,
    )

with DAG(
    'meltano_EL_run_dag',
    default_args=default_args,
    description='A DAG to run EL Meltano',
    schedule_interval='@daily',  # Trigger manually or adjust as needed
    start_date=datetime(2025, 1, 1),
    concurrency=1,
    catchup=False,
    tags=['meltano', 'docker']
) as dag:
    
    update_json_task = PythonOperator(
        task_id='update_json_data_path',
        python_callable=update_data_path,
        provide_context=True,
        dag=dag
    )

    with TaskGroup("extractions", tooltip="Extraction tasks") as extraction_group:
        # Task to extract northwind database from postgres to CSV
        extract_postgres = meltano_task(
            task_id='extract_postgres',
            entrypoint="meltano run tap-postgres target-csv",
            # Mount to sync local folder to meltano container folder
            mounts=[Mount(source=f'{path_airflow_folder}/postgres', target='/data_extraction', type='bind')],
            dag=dag,
        )
        # Task to extract order_details data from CSV to CSV
        extract_csv = meltano_task(
            task_id='extract_csv',
            entrypoint=[
                "sh", "-c",
                "meltano config tap-csv set csv_files_definition 'files_def.json' && "
                "meltano config tap-csv set add_metadata_columns false && "
                "meltano config target-csv set output_path '/csv' && "
                "meltano run tap-csv target-csv"
            ],
            mounts=[
                # Mount to sync local folder to meltano container folder
                Mount(source=f'{path_airflow_folder}/csv', target='/csv', type='bind'),
                Mount(source=f'{path_airflow_folder}/data', target='/output', type='bind')
                ],
            dag=dag,
        )


    with TaskGroup("loader", tooltip="loader tasks") as loader_group:
        load_to_postgres = meltano_task(
            task_id='load_to_postgres',
            entrypoint=[
                "sh", "-c",
                "meltano config tap-csv set csv_files_definition '/script/csv_load_files_def.json' && "
                "meltano config tap-csv set add_metadata_columns false && "
                "meltano run tap-csv target-postgres"
            ],
            # Mount to sync local folder to meltano container folder
            mounts=[
                Mount(source=f'{path_airflow_folder}/csv', target='/csv', type='bind'),
                Mount(source=f'{path_airflow_folder}/postgres', target='/postgres', type='bind'),
                Mount(source=f'{path_airflow_folder}/dags', target='/script', type='bind')
                ],
            dag=dag,
        )

    update_json_task >> extraction_group >> loader_group