resource "aws_s3_bucket" "uploads" {
  bucket = "${var.project_name}-uploads-${data.aws_caller_identity.current.account_id}"
  acl    = "private"

  lifecycle_rule {
    enabled = true
    expiration {
      days = 3650
    }
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

data "aws_caller_identity" "current" {}
