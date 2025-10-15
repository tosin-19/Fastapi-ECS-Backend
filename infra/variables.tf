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

variable "container_port" {
  description = "Port exposed by the container"
  default     = 8080
}

variable "image_uri" {
  description = "Docker image URI to use in ECS task definition"
  type        = string
}
