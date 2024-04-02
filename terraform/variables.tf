variable "credentials" {
  description = "My GCP Credentials"
  default     = "./keys/my-creds.json"
}

variable "project" {
  description = "Project"
  default     = "oceanic-facet-418014"
}

variable "region" {
  description = "Project region"
  default     = "europe-west2-a"
}

variable "location" {
  description = "Project Location"
  default     = "EU"
}

variable "bq_table_name" {
  description = "UK Approved Food Establishments Dataset BigQuery Table"
  default     = "approved_food_establishments"
}

variable "bq_dataset_id" {
    description = "The ID of the BigQuery dataset where the table will be created."
    type        = string
    default     = "approved_food_establishments_34421"
}

variable "gcs_bucket_name" {
  description = "UK Approved Food Establishments Bucket"
  default     = "approved-food-establishments-bucket"
}

variable "gcp_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}