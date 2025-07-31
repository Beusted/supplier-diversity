from aws_cdk import (
    Stack,
    aws_amplify_alpha as amplify,
    aws_codebuild as codebuild,
    CfnOutput,
    SecretValue,
)
from constructs import Construct


class SupplierDiversityAmplifyStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create Amplify App (like Vercel project)
        amplify_app = amplify.App(
            self, "SupplierDiversityApp",
            app_name="supplier-diversity-dashboard",
            description="Small Business PO Percentage Dashboard - Cal Poly SLO AI Summer Camp",
            
            # GitHub integration (like Vercel)
            source_code_provider=amplify.GitHubSourceCodeProvider(
                owner="Beusted",
                repository="supplier-diversity",
                oauth_token=SecretValue.secrets_manager("github-token")  # Store GitHub token in Secrets Manager
            ),
            
            # Build settings for Streamlit
            build_spec=codebuild.BuildSpec.from_object({
                "version": 1,
                "applications": [{
                    "frontend": {
                        "phases": {
                            "preBuild": {
                                "commands": [
                                    "pip install -r requirements.txt"
                                ]
                            },
                            "build": {
                                "commands": [
                                    # Convert Streamlit to static or run as SPA
                                    "streamlit run run_po_dashboard.py --server.headless true --server.port 3000"
                                ]
                            }
                        },
                        "artifacts": {
                            "baseDirectory": "/",
                            "files": ["**/*"]
                        }
                    }
                }]
            }),
            
            # Environment variables
            environment_variables={
                "AMPLIFY_MONOREPO_APP_ROOT": "/",
                "AMPLIFY_DIFF_DEPLOY": "false",
                "_LIVE_UPDATES": '[{"name":"Streamlit","pkg":"streamlit","type":"npm","version":"latest"}]'
            }
        )

        # Add main branch (like Vercel production)
        main_branch = amplify_app.add_branch(
            "main",
            branch_name="main",
            auto_build=True,  # Auto-deploy on push
            stage="PRODUCTION"
        )

        # Add custom domain (optional)
        # domain = amplify_app.add_domain(
        #     "supplier-diversity.yourdomain.com",
        #     sub_domain_settings=[
        #         amplify.SubDomainSetting(
        #             branch=main_branch,
        #             prefix=""
        #         )
        #     ]
        # )

        # Outputs (like Vercel deployment URLs)
        CfnOutput(
            self, "AmplifyAppUrl",
            value=f"https://main.{amplify_app.app_id}.amplifyapp.com",
            description="Live URL of your Supplier Diversity Dashboard"
        )

        CfnOutput(
            self, "AmplifyAppId",
            value=amplify_app.app_id,
            description="Amplify App ID"
        )

        CfnOutput(
            self, "AmplifyConsoleUrl",
            value=f"https://console.aws.amazon.com/amplify/home#/{amplify_app.app_id}",
            description="Amplify Console URL for managing deployments"
        )
