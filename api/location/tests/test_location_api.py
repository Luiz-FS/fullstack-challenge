from http import HTTPStatus
import pytest
from core import serializers, models


@pytest.mark.django_db
class TestList:

    def test_list_locations(self, client, make_locations, authenticator_mock):
        # arrange
        authenticator_mock(success=True)
        expected_locations = serializers.LocationSerializer(make_locations, many=True).data
        expected_locations = sorted(expected_locations, key=lambda location: location["name"])

        # act
        response = client.get("/api/location/")
        data = response.json()

        #assert
        assert expected_locations == data["results"]

    def test_list_locations_unauthorized(self, client, authenticator_mock):
        # arrange
        authenticator_mock(success=False)

        # act
        response = client.get("/api/location/")

        # assert
        assert response.status_code == HTTPStatus.UNAUTHORIZED



@pytest.mark.django_db
class TestCreate:
    def test_create_location(self, client, authenticator_mock):
        # arrange
        authenticator_mock(success=True)

        # act
        response = client.post("/api/location/", {
            "name": "loc test",
            "coordinate_x": 20,
            "coordinate_y": 30
        }, content_type="application/json")
        data = response.json()

        location = models.Location.objects.get(id=data["id"])
        location_raw = serializers.LocationSerializer(location).data
        
        #assert
        assert data == location_raw
    
    def test_list_locations_unauthorized(self, client, authenticator_mock):
        # arrange
        authenticator_mock(success=False)

        # act
        response = client.post("/api/location/", {
            "name": "loc test",
            "coordinate_x": 20,
            "coordinate_y": 30
        }, content_type="application/json")

        # assert
        assert response.status_code == HTTPStatus.UNAUTHORIZED



@pytest.mark.django_db
class TestListNeighbors:
    def test_list_neighbors_locations(self, client, make_locations, authenticator_mock, filter_neighbors):
        # arrange
        authenticator_mock(success=True)
        x, y, d_max = 15, 20, 20
        expected_locations = filter_neighbors(make_locations, x, y, d_max)
        expected_locations = serializers.LocationNeighborsSerializer(expected_locations, many=True).data
        expected_locations = sorted(expected_locations, key=lambda location: location["name"])
        
        for location in expected_locations:
            location["distance"] = int(location["distance"])

        # act
        response = client.get(f"/api/location/neighbors/?x={x}&y={y}&d-max={d_max}")
        results = response.json()["results"]

        for location in results:
            location["distance"] = int(location["distance"])

        #assert
        assert expected_locations == results
    
    def test_list_neighbors_locations_empty(self, client, make_locations, authenticator_mock):
        # arrange
        authenticator_mock(success=True)
        x, y, d_max = 15, 20, 1

        # act
        response = client.get(f"/api/location/neighbors/?x={x}&y={y}&d-max={d_max}")
        results = response.json()["results"]

        #assert
        assert results == []
    
    def test_list_neighbors_locations_unauthorized(self, client, authenticator_mock):
        # arrange
        authenticator_mock(success=False)
        x, y, d_max = 15, 20, 1

        # act
        response = client.get(f"/api/location/neighbors/?x={x}&y={y}&d-max={d_max}")

        # assert
        assert response.status_code == HTTPStatus.UNAUTHORIZED