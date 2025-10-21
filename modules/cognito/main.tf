resource "aws_cognito_user_pool" "pool" {
  name = "${var.project_name}-user-pool"

  alias_attributes = ["preferred_username"]

  auto_verified_attributes = ["email"]
  
  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_uppercase = true
    require_numbers   = true
    require_symbols   = false
  }

  admin_create_user_config {
    allow_admin_create_user_only = false
  }

  email_configuration {
    email_sending_account = "COGNITO_DEFAULT"
  }

  schema {
    name                = "email"
    attribute_data_type = "String"
    required            = true
    mutable             = false
  }

  schema {
    name                = "given_name" 
    attribute_data_type = "String"
    required            = true
    mutable             = true
  }

  schema {
    name                = "family_name" 
    attribute_data_type = "String"
    required            = true
    mutable             = true
  }

  schema {
    name                = "birthdate"
    attribute_data_type = "String"
    required            = false
    mutable             = true
  }
  
  schema {
    name                = "role"
    attribute_data_type = "String"
    required            = false
    mutable             = true
  }
}

resource "aws_cognito_user_pool_client" "client" {
  name = "${var.project_name}-app-client"

  user_pool_id = aws_cognito_user_pool.pool.id
}