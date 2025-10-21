# Songify

## Setup

- Crate a new file or rename `.env.example` to `.env` and update the variables

### Terraform

- Update variables in `config.s3.tfbackend`
- Run `terraform init -backend-config='./config.s3.tfbackend'`
- Run `terraform apply` and check if the changes are acceptable