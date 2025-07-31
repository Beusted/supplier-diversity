#!/usr/bin/env python3
import os
import aws_cdk as cdk
from cdk.supplier_diversity_stack import SupplierDiversityStack


app = cdk.App()
SupplierDiversityStack(app, "SupplierDiversityStack",
    # Specify the AWS region
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region=os.getenv('CDK_DEFAULT_REGION', 'us-west-2')
    ),
    description="Supplier Diversity Dashboard - Small Business PO Percentage Analysis"
)

app.synth()
