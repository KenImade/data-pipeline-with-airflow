# Data Pipeline with Airflow

The aim of this project was to learn how to build a data pipeline using Airflow for workflow orchestration and Terraform to set up the infrastructure.

## Project Structure
```
/my_data_pipeline_project
|-- /airflow
|   |-- /dags
|   |   `-- food_dag.py
|-- /terraform
|   |-- main.tf
    |-- variables.tf
|   `-- schema.json
`-- Dockerfile
```

## How to Run Project
To run this project you will need the following prerequisites
- A Google Cloud Service account which has BigQuery, Storage Admin roles enabled.
- Docker
- Docker-Compose
- Terraform

1. Clone the github repo.
```
git clone https://github.com/KenImade/data-pipeline-with-airflow
```
2. cd into the terraform folder.
```
cd terraform
```
3. Create a folder called **keys**
```
mkdir keys
```
4. Place the Google Service Account key json file into the keys directory.
```
keys/my-creds.json
```
4. Run terraform init
```
terraform init
```
5. Run terraform apply,
```
terraform apply
```
6. cd into the airflow folder.
```
cd .. && cd airflow
```
7. Run docker build naming the image whatever you want.
```
docker build . --tag your-chosen-name:latest
```
8. Run docker compose.
```
docker-compose up -d
```
9. Input airflow credentials (username: airflow, password: airflow).

10. Setup Airflow connection to Google Cloud by copying the contents of the my-cred.json file.

11. Run the pipeline.
