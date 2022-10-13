from core import models
from django.db.models import F, query
from django.db.models.functions import Power, Sqrt


class LocationRepository:
    @staticmethod
    def get_neighbors_locations(coordinate_x: int, coordinate_y: int, d_max: int) -> query.QuerySet:
        return models.Location.objects.annotate(
            distance=Sqrt(
                Power(
                    F("coordinate_x") - coordinate_x,
                    2
                ) +
                Power(
                    F("coordinate_y") - coordinate_y,
                    2
                )
            )
        ).filter(distance__lte=d_max).order_by("name")