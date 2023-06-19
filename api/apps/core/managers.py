"""
Core app model managers
"""
from django.db import models


class ActiveManager(models.Manager):
    """
    Active records model manager
    """

    def get_queryset(self):
        return super().get_queryset().filter(archived=False)


class ArchivedManager(models.Manager):
    """
    Inactive records model manager
    """

    def get_queryset(self):
        return super().get_queryset().filter(archived=True)
