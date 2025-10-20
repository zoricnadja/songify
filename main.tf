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