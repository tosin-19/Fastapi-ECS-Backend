# ========================
# AWS Provider
# ========================
provider "aws" {
  region = "us-east-1"   # Change if needed
}

# ========================
# Use Default VPC
# ========================
data "aws_vpc" "default" {
  default = true
}

data "aws_subnet_ids" "default" {
  vpc_id = data.aws_vpc.default.id
}

# ========================
# ECS Cluster
# ========================
resource "aws_ecs_cluster" "main" {
  name = "myapp-cluster"
}

# ========================
# IAM Role for ECS Task
# ========================
resource "aws_iam_role" "ecs_task_execution" {
  name = "ecsTaskExecutionRole"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
}

# Attach AWS managed policy for ECS tasks
resource "aws_iam_role_policy_attachment" "ecs_task_execution_policy" {
  role       = aws_iam_role.ecs_task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# ========================
# ECS Task Definition
# ========================
resource "aws_ecs_task_definition" "app" {
  family                   = "myapp-task"
  cpu                      = "256"
  memory                   = "512"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn

  container_definitions = jsonencode([
    {
      name      = "myapp"
      image     = "<611837360680.dkr.ecr.eu-north-1.amazonaws.com/myapp>:latest"
