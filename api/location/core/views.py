from core import models, repositories, serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from middlewares.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response


class LocationViewSet(viewsets.ModelViewSet):
    queryset = models.Location.objects.all().order_by('name')
    serializer_class = serializers.LocationSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter("x", OpenApiTypes.INT32, OpenApiParameter.QUERY),
            OpenApiParameter("y", OpenApiTypes.INT32, OpenApiParameter.QUERY),
            OpenApiParameter("d-max", OpenApiTypes.INT32, OpenApiParameter.QUERY)
        ],
        responses=serializers.LocationNeighborsSerializer
    )
    @action(detail=False, methods=["GET"])
    def neighbors(self, request: Request, pk: str=None) -> Response:
        coordinate_x = int(request.query_params["x"])
        coordinate_y = int(request.query_params["y"])
        d_max = int(request.query_params["d-max"])

        queryset = repositories.LocationRepository.get_neighbors_locations(coordinate_x, coordinate_y, d_max)
        page = self.paginate_queryset(queryset)

        serializer = serializers.LocationNeighborsSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
