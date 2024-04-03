# Data Pipeline with Airflow

The aim of this project was to learn how to build a data pipeline using Airflow for workflow orchestration and Terraform to set up the infrastructure.

## Project Structure
```
/my_data_pipeline_project
|-- /airflow
|   |-- /dags
|   |   `-- data_pipeline.py
|   `-- /scripts
|       |-- clean_data.py
|       `-- convert_to_parquet.py
|-- /terraform
|   |-- bigquery.tf
|   `-- schema.json
`-- Dockerfile
```
