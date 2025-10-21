terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.17.0"
    }
  }

  backend "s3" {
    bucket       = ""
    key          = ""
    region       = ""
    use_lockfile = true
  }
}

provider "aws" {
  region = var.region
}

module "dynamodb" {
  source = "./modules/dynamodb"

  project_name   = var.project_name
  read_capacity  = var.dynamodb_read_capacity
  write_capacity = var.dynamodb_write_capacity
}