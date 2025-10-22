#!/usr/bin/env python3
import os

import aws_cdk as cdk
from stacks import BackendStack

app = cdk.App()
BackendStack(app, "BackendStack",
             project_name="songify",
             read_capacity=1,
             write_capacity=1)

app.synth()
