from aws_cdk import (
    Stack,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_ecs_patterns as ecs_patterns,
    aws_logs as logs,
    CfnOutput,
)
from constructs import Construct


class SupplierDiversityECSStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create VPC
        vpc = ec2.Vpc(
            self, "SupplierDiversityVPC",
            max_azs=2,  # Use 2 availability zones
            nat_gateways=1  # Cost optimization
        )

        # Create ECS Cluster
        cluster = ecs.Cluster(
            self, "SupplierDiversityCluster",
            vpc=vpc,
            cluster_name="supplier-diversity-cluster"
        )

        # Create Fargate Service with Load Balancer
        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "SupplierDiversityService",
            cluster=cluster,
            memory_limit_mib=512,
            cpu=256,
            desired_count=1,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                # This would use your Docker image
                image=ecs.ContainerImage.from_asset(".."),  # Points to your app directory
                container_port=8080,
                log_driver=ecs.LogDrivers.aws_logs(
                    stream_prefix="supplier-diversity",
                    log_retention=logs.RetentionDays.ONE_WEEK
                ),
                environment={
                    "PORT": "8080",
                    "STREAMLIT_SERVER_PORT": "8080",
                    "STREAMLIT_SERVER_ADDRESS": "0.0.0.0",
                    "STREAMLIT_SERVER_HEADLESS": "true"
                }
            ),
            public_load_balancer=True,
            protocol=ecs_patterns.ApplicationProtocol.HTTP
        )

        # Configure health check
        fargate_service.target_group.configure_health_check(
            path="/",
            healthy_http_codes="200"
        )

        # Output the load balancer URL
        CfnOutput(
            self, "LoadBalancerURL",
            value=f"http://{fargate_service.load_balancer.load_balancer_dns_name}",
            description="URL of the Supplier Diversity Dashboard"
        )

        # Output the service ARN
        CfnOutput(
            self, "ServiceArn",
            value=fargate_service.service.service_arn,
            description="ARN of the ECS Fargate service"
        )
