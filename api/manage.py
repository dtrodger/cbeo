#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import pathlib

from django.core.management import execute_from_command_line
from dotenv import load_dotenv


ENVIRONMENT_FOLDER_PATH = pathlib.Path() / "env"


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    if len(sys.argv) > 2 and sys.argv[1] == "-e":
        envs = ["local", "qa", "stagging", "prod", "docker_local"]
        env = sys.argv[2]
        if env not in envs:
            raise ValueError(f"Incorrect environment '{env}''. Options include {envs}")

        sys.argv.remove("-e")
        sys.argv.remove(env)
    else:
        env = "local"

    if env == "local":
        load_dotenv(ENVIRONMENT_FOLDER_PATH / ".env.local")
    if env == "docker_local":
        load_dotenv(ENVIRONMENT_FOLDER_PATH / ".env.docker_local")
    elif env == "qa":
        load_dotenv(ENVIRONMENT_FOLDER_PATH / ".env.sbx")
    elif env == "stagging":
        load_dotenv(ENVIRONMENT_FOLDER_PATH / ".env.stagging")
    elif env == "prod":
        load_dotenv(ENVIRONMENT_FOLDER_PATH / ".env.prod")

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
