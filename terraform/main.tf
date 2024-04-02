terraform {
    required_providers {
        google = {
            source = "hashicorp/google"
            version = "5.6.0"
        }
      
    }
}

provider "google" {
  credentials = file(var.credentials)
  project     = var.project
  region      = var.region
}

resource "google_storage_bucket" "approved-food-establishments-bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "approved_food_establishments_dataset" {
  project = var.project
  dataset_id = var.bq_dataset_id
}

resource "google_bigquery_table" "approved_food_establishments" {
  dataset_id = google_bigquery_dataset.approved_food_establishments_dataset.dataset_id
  table_id   = var.bq_table_name
  schema     = file("schema.json")
}
