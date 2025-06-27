from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'deep',
    'depends_on_past': False,
    'email_on_failure': True,
    'email': ['mangroliyadeep@gmail.com'],
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'start_date': datetime(2025, 1, 1)
}

with DAG('bizsight_pipeline',
         default_args=default_args,
         description='Full Bizsight ETL + ML Pipeline',
         schedule_interval='@daily',
         catchup=False) as dag:

    create_raw_db = BashOperator(
        task_id='create_raw_db',
        bash_command='python /Users/deepmangroliya/Desktop/d2p_ds_project/src/database.py -dbn True -db "raw"'
    )

    load_raw_data = BashOperator(
        task_id='load_data_raw_db',
        bash_command='python /Users/deepmangroliya/Desktop/d2p_ds_project/src/database.py -db "raw" -t "upload-to-database"'
    )

    run_etl = BashOperator(
        task_id='run_etl_pipeline',
        bash_command='python /Users/deepmangroliya/Desktop/d2p_ds_project/src/etl_pipeline.py'
    )

    create_refined_db = BashOperator(
        task_id='create_refined_db',
        bash_command='python /Users/deepmangroliya/Desktop/d2p_ds_project/src/database.py -dbn True -db "refined"'
    )

    load_cleaned_data = BashOperator(
        task_id='load_data_refined_db',
        bash_command='python /Users/deepmangroliya/Desktop/d2p_ds_project/src/database.py -db "refined" -t "cleaned-upload-to-database"'
    )

    run_data_analysis = BashOperator(
        task_id='run_data_analysis_task',
        bash_command='python3 /Users/deepmangroliya/Desktop/d2p_ds_project/main.py -t "data_analysis_ext"'
    )

    run_modeling = BashOperator(
        task_id='run_modeling_task',
        bash_command='python3 /Users/deepmangroliya/Desktop/d2p_ds_project/main.py -t "modeling"'
    )

    # DAG flow
    create_raw_db >> load_raw_data >> run_etl >> create_refined_db >> load_cleaned_data >> run_data_analysis >> run_modeling
