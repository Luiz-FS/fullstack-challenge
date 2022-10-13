from core import models
from rest_framework import serializers


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = "__all__"


class LocationNeighborsSerializer(LocationSerializer):
    distance = serializers.SerializerMethodField(read_only=True)

    def get_distance(self, obj) -> int:
        return obj.distance
