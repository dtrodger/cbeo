"""
AWS API
"""

import os
import json

import boto3

from api.utils import get_env_var


def aws_client(service, region_name="us-west-1", **kwargs):
    """
    Gets an AWS service client
    """

    return boto3.client(
        service,
        region_name=region_name,
        aws_access_key_id=get_env_var("AWS_ACCESS_KEY"),
        aws_secret_access_key=get_env_var("AWS_SECRET_ACCESS_KEY"),
        **kwargs,
    )


def aws_resource(service, region_name="us-west-1", **kwargs):
    """
    Gets an AWS resource
    """

    return boto3.resource(
        service,
        region_name=region_name,
        aws_access_key_id=get_env_var("AWS_ACCESS_KEY"),
        aws_secret_access_key=get_env_var("AWS_SECRET_ACCESS_KEY"),
        **kwargs,
    )


def secrets_manager_client():
    """
    Gets an AWS Secrets Manager client
    """

    return aws_client("secretsmanager")


def aws_secret(secret_name):
    """
    Gets AWS secrets from Secrets Manager
    """

    return json.loads(
        secrets_manager_client().get_secret_value(SecretId=secret_name)["SecretString"]
    )


def aws_secret_to_env():
    """
    Gets AWS secrets and set them to env vars
    """
    if get_env_var("ENVIRONMENT") != "local" and get_env_var("AWS_SECRET"):
        for secret_name, secret_value in aws_secret(get_env_var("AWS_SECRET")).items():
            os.environ[secret_name] = str(secret_value)
