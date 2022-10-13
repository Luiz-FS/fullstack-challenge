import uuid

from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Location(BaseModel):
    name = models.CharField(max_length=255, null=False)
    coordinate_x = models.PositiveIntegerField(null=False)
    coordinate_y = models.PositiveIntegerField(null=False)
