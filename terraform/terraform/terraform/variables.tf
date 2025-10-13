variable "aws_region" { default = "us-east-1" }
variable "project_name" { default = "backend-files" }
variable "vpc_id" { type = string, default = "" } # optional, or create new VPC resources
# provide cluster size, etc as needed
