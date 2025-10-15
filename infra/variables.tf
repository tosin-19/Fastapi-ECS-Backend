variable "region" {
  description = "AWS region to deploy resources"
  default     = "us-east-1"
}

variable "cluster_name" {
  description = "ECS cluster name"
  default     = "myapp-cluster"
}

variable "service_name" {
  description = "ECS service name"
  default     = "myapp-service"
}

variable "container_name" {
  description = "Name of the container"
  default     = "myapp"
}

variable "container_image" {
  description = "ECR image URI for the container (e.g., 123456789012.dkr.ecr.us-east-1.amazonaws.com/myapp:latest)"
  default     = "YOUR_ECR_REPO_URI:latest"
}

variable "container_port" {
  description = "Port exposed by the container"
  default     = 8080
}

variable "image_uri" {
  description = "ECR image URI for the ECS task"
  type        = string
}
