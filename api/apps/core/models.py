"""
Core app models
"""
from django.db import models
from rest_framework import serializers

from apps.core.managers import (
    ActiveManager,
    ArchivedManager
)

class BaseModel(models.Model):
    """
    Abstract base model
    """

    class Meta:
        abstract = True

    archived = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    objects = ActiveManager()
    archived_objects = ArchivedManager()
    all_objects = models.Manager()

    @classmethod
    def serializer(cls, serializer_fields="__all__", serializer_depth=0):
        """
        Class factory to dynamically create DRF serializers
        """

        class ModelSerializer(serializers.ModelSerializer):
            """
            Arbitrary model serializer
            """

            class Meta:
                model = cls
                fields = serializer_fields
                depth = serializer_depth

        return ModelSerializer

    @classmethod
    def serialize_many(cls, models, serializer_fields="__all__", serializer_depth=3):
        """
        Serialize a batch of models
        """

        return cls.serializer(serializer_fields, serializer_depth)(
            models, many=True
        ).data

    def serialize(self, serializer_fields="__all__", serializer_depth=3):
        """
        Serializer
        """

        return self.serializer(serializer_fields, serializer_depth)(self).data


class Pitch(BaseModel):
    """
    Pitch model
    """

    def upload_to_media_upload_path(instance, filename):
        """
        Upload path constructor
        """

        return f"pitch/{filename}"

    file = models.FileField(upload_to=upload_to_media_upload_path, null=False)
    file_name = models.CharField(null=True, max_length=256)
    symbol_clear_message_count = models.IntegerField(default=0)
    add_order_message_count = models.IntegerField(default=0)
    modify_order_message_count = models.IntegerField(default=0)
    execute_order_message_count = models.IntegerField(default=0)
    trade_message_count = models.IntegerField(default=0)
    trade_break_message_count = models.IntegerField(default=0)
    cancel_order_message_count = models.IntegerField(default=0)
    trading_status_message_count = models.IntegerField(default=0)
    auction_update_message_count = models.IntegerField(default=0)
    auction_summary_message_count = models.IntegerField(default=0)
    retail_price_improvement_message_count = models.IntegerField(default=0)
