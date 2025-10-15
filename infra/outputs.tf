output "cluster_name" {
  value = aws_ecs_cluster.main.name
}

output "service_name" {
  value = aws_ecs_service.app_service.name
}

output "task_definition" {
  value = aws_ecs_task_definition.app.family
}
