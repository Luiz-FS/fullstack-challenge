import pytest
from core.repositories import LocationRepository


@pytest.mark.django_db
class TestLocationRepository:
    def test_get_neighbors_locations(self, make_locations, filter_neighbors):
        # arrange
        x, y, d_max = 15, 20, 20
        expected_locations = filter_neighbors(make_locations, x, y, d_max)
        expected_locations = sorted(expected_locations, key=lambda location: location.name)

        # act
        locations = list(LocationRepository.get_neighbors_locations(x, y, d_max))

        # assert
        assert locations == expected_locations
    
    def test_get_neighbors_locations_empty(self, make_locations):
        # arrange
        x, y, d_max = 15, 20, 1

        # act
        locations = list(LocationRepository.get_neighbors_locations(x, y, d_max))

        # assert
        assert locations == []

