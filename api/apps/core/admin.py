"""
Core app admin
"""

from django.contrib import admin

from apps.core.models import Pitch


@admin.register(Pitch)
class PitchAdmin(admin.ModelAdmin):
    """
    Pitch admin
    """
