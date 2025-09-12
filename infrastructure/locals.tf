data "aws_caller_identity" "current" {}

locals {
    user_data_script = templatefile("${path.module}/scripts/script.tpl", {
    AWS_REGION       = var.aws_region
    AWS_ACCOUNT_ID   = data.aws_caller_identity.current.account_id
    ECR_REPOSITORY   = var.ecr_repository
  })
}