from aws_cdk import (
    Stack,
    aws_apprunner as apprunner,
    aws_iam as iam,
    CfnOutput,
    CfnParameter,
)
from constructs import Construct


class SupplierDiversityStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Parameter for GitHub connection ARN (to be created manually first)
        github_connection_arn = CfnParameter(
            self, "GitHubConnectionArn",
            type="String",
            description="ARN of the GitHub connection for App Runner",
            default="arn:aws:apprunner:us-west-2:123456789012:connection/supplier-diversity-github"
        )

        # Create IAM role for App Runner instance
        instance_role = iam.Role(
            self, "AppRunnerInstanceRole",
            assumed_by=iam.ServicePrincipal("tasks.apprunner.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess")
            ]
        )

        # App Runner service configuration
        app_runner_service = apprunner.CfnService(
            self, "SupplierDiversityService",
            service_name="supplier-diversity-dashboard",
            source_configuration=apprunner.CfnService.SourceConfigurationProperty(
                auto_deployments_enabled=True,
                code_repository=apprunner.CfnService.CodeRepositoryProperty(
                    repository_url="https://github.com/Beusted/supplier-diversity",
                    source_code_version=apprunner.CfnService.SourceCodeVersionProperty(
                        type="BRANCH",
                        value="main"
                    ),
                    code_configuration=apprunner.CfnService.CodeConfigurationProperty(
                        configuration_source="CONFIGURATION_FILE"  # Uses apprunner.yaml
                    )
                ),
                authentication_configuration=apprunner.CfnService.AuthenticationConfigurationProperty(
                    connection_arn=github_connection_arn.value_as_string
                )
            ),
            instance_configuration=apprunner.CfnService.InstanceConfigurationProperty(
                cpu="0.25 vCPU",
                memory="0.5 GB",
                instance_role_arn=instance_role.role_arn
            ),
            health_check_configuration=apprunner.CfnService.HealthCheckConfigurationProperty(
                protocol="HTTP",
                path="/",
                interval=10,
                timeout=5,
                healthy_threshold=1,
                unhealthy_threshold=5
            )
        )

        # Output the service URL
        CfnOutput(
            self, "ServiceUrl",
            value=f"https://{app_runner_service.attr_service_url}",
            description="URL of the deployed Supplier Diversity Dashboard"
        )

        # Output the service ARN
        CfnOutput(
            self, "ServiceArn",
            value=app_runner_service.attr_service_arn,
            description="ARN of the App Runner service"
        )

        # Output instructions
        CfnOutput(
            self, "Instructions",
            value="After deployment, visit the service URL to access your Small Business PO Percentage Dashboard",
            description="Next steps"
        )
