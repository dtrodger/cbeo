"""
Management command to run the API in a Docker container
"""

import logging

from django.core.management.base import BaseCommand
from django.core.management import call_command


log = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Management command to bootstrap the database
    """

    def handle(self, *args, **options):
        """
        Command handler
        """
        call_command("migrate", "--noinput")
        call_command("collectstatic", "--noinput")
        call_command("runserver", "0.0.0.0:8001")
