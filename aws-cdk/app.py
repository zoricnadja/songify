#!/usr/bin/env python3
import os

from aws_cdk import App
from stacks import BackendStack

app = App()
BackendStack(app, "BackendStack",
             project_name="songify",
             read_capacity=1,
             write_capacity=1)

app.synth()
