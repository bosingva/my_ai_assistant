terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.3"
    }
  }
}

terraform {
  backend "s3" {
    bucket         = "dk-s3-for-terraform-state"
    key            = "ai-assisnant/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "ai-assisnant-terraform-lock"
    encrypt        = true
  }
}