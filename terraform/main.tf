# Terraform configuration for App Runner (CDK alternative)
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-west-2"
}

# GitHub connection
resource "aws_apprunner_connection" "github" {
  connection_name = "supplier-diversity-github"
  provider_type   = "GITHUB"

  tags = {
    Name = "Supplier Diversity GitHub Connection"
  }
}

# App Runner service
resource "aws_apprunner_service" "supplier_diversity" {
  service_name = "supplier-diversity-dashboard"

  source_configuration {
    auto_deployments_enabled = true
    
    code_repository {
      repository_url = "https://github.com/Beusted/supplier-diversity"
      
      source_code_version {
        type  = "BRANCH"
        value = "main"
      }
      
      code_configuration {
        configuration_source = "CONFIGURATION_FILE"
      }
    }
    
    authentication_configuration {
      connection_arn = aws_apprunner_connection.github.arn
    }
  }

  instance_configuration {
    cpu    = "0.25 vCPU"
    memory = "0.5 GB"
  }

  health_check_configuration {
    protocol            = "HTTP"
    path                = "/"
    interval            = 10
    timeout             = 5
    healthy_threshold   = 1
    unhealthy_threshold = 5
  }

  tags = {
    Name = "Supplier Diversity Dashboard"
    Project = "Cal Poly SLO AI Summer Camp"
  }
}

# Outputs
output "service_url" {
  description = "URL of the deployed dashboard"
  value       = "https://${aws_apprunner_service.supplier_diversity.service_url}"
}

output "service_arn" {
  description = "ARN of the App Runner service"
  value       = aws_apprunner_service.supplier_diversity.arn
}
