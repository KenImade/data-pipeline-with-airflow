from airflow import DAG

from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'kenneth',
    'retry': 5,
    'retry_delay': timedelta(minutes=5)
}

def clean_data():
    import pandas as pd

    file_path = "/opt/airflow/data/data.csv"
    df = pd.read_csv(file_path)

    # combine address
    df['Address'] = df['Address1'].fillna('').astype(str) + ' ' + df['Address2'].fillna('').astype(str) + ' ' + df['Address3'].fillna('').astype(str)
    df = df.drop(columns=['Address1','Address2','Address3'])

    # keep relevant columns
    columns = ['AppNo','TradingName','Town','Postcode','Country','All_Activities','Species','Remarks','CompetentAuthority', 'GeographicLocalAuthority', 'X', 'Y', 'AddressWithheld', 'Address']
    df = df[columns].copy()

    df.to_csv('/opt/airflow/data/clean_data.csv')

def convert_data():
    import pandas as pd
    
    csv_file_path = '/opt/airflow/data/clean_data.csv'
    parquet_file_path = '/opt/airflow/data/data.parquet'

    df = pd.read_csv(csv_file_path)
    df.to_parquet(parquet_file_path, engine='pyarrow', index=False)


with DAG(
    dag_id='food_pipeline_dag_v03.2',
    default_args=default_args,
    description="DAG description of food data ingestion pipeline",
    start_date=datetime(2024, 4, 2),
    schedule_interval='@monthly'
) as dag:
    download_data = BashOperator(
        task_id='download_data',
        bash_command="mkdir -p /opt/airflow/data && wget https://fsa-catalogue2.s3.eu-west-2.amazonaws.com/Approved+establishments+01-03-2024.csv -O /opt/airflow/data/data.csv"
    )
    clean_data = PythonOperator(
        task_id='clean_data',
        python_callable=clean_data
    )
    convert_data = PythonOperator(
        task_id='convert_data',
        python_callable=convert_data
    )
    upload_data_to_gcs = LocalFilesystemToGCSOperator(
        task_id='upload_data_to_gcs',
        src='/opt/airflow/data/data.parquet',
        dst='approved-food-establishments-bucket/food_data/data.parquet',
        bucket='approved-food-establishments-bucket',
        mime_type='application/octet-stream'
    )
    load_gcs_to_bigquery = GCSToBigQueryOperator(
        task_id='load_gcs_to_bigquery',
        bucket='approved-food-establishments-bucket',
        source_objects=['approved-food-establishments-bucket/food_data/data.parquet'],
        destination_project_dataset_table='oceanic-facet-418014.approved_food_establishments_34421.approved_food_establishments',
        source_format='PARQUET',
        write_disposition='WRITE_TRUNCATE',  # Use WRITE_APPEND to append data or WRITE_EMPTY to only write if the table is empty
        create_disposition='CREATE_IF_NEEDED',  # Creates the table if it doesn't exist
        # Set to False if the table does not have a schema defined
        autodetect=True,  # BigQuery attempts to automatically detect the schema
    )


    download_data >> clean_data >> convert_data >> upload_data_to_gcs >> load_gcs_to_bigquery

