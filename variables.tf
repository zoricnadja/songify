variable "region" {
  description = "AWS region to deploy resources in."
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "The name of the project."
  type        = string
  default     = "songify"
}

variable "dynamodb_read_capacity" {
  description = "Read capacity units for the DynamoDB table."
  type        = number
  default     = 1
}

variable "dynamodb_write_capacity" {
  description = "Write capacity units for the DynamoDB table."
  type        = number
  default     = 1
}