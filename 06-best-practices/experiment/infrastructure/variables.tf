variable "aws_region" {
  description = "AWS region to create resources"
  default     = "us-east-2"
}

variable "project_id" {
  description = "Project_id"
  default = "mlops-zoomcamp"
}

variable "source_stream_name" {
  description = "Source stream name"
  default = "ride-events-stg"

}