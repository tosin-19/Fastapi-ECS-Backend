###############################################
# AWS Provider
###############################################
provider "aws" {
  region = "us-east-1" # Change if needed
}

###############################################
# Use Default VPC and Subnets
###############################################
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

###############################################
# ECS Cluster
###############################################
resource "aws_ecs_cluster" "main" {
  name = "myapp-cluster"
}

###############################################
# IAM Role for ECS Task Execution
###############################################
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

# Attach ECS Task Execution Policy
resource "aws_iam_role_policy_attachment" "ecs_task_execution_policy" {
  role       = aws_iam_role.ecs_task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

###############################################
# ECS Task Definition
###############################################
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
      image     = "611837360680.dkr.ecr.eu-north-1.amazonaws.com/myapp:latest" # Replace with your real ECR URL
      essential = true
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
        }
      ]
    }
  ])
}

###############################################
# ECS Service (Optional - Run your task)
###############################################
resource "aws_ecs_service" "app_service" {
  name            = "myapp-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = data.aws_subnets.default.ids
    assign_public_ip = true
  }

  depends_on = [aws_ecs_task_definition.app]
}
