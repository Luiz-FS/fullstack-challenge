import math
from sre_constants import SUCCESS
import pytest
from core.models import Location


class ResponseMock:
    status_code = 200

    def __init__(self, status_code):
        self.status_code = status_code

    def json(self):
        return {}


class RequestMock:
    headers = {}
    session = {}

    def __init__(self, headers, session):
        self.headers = headers
        self.session = session


def point_distance(coor_x1, coor_y1, location):
    distance = math.sqrt((coor_x1 - location.coordinate_x)**2 + (coor_y1 - location.coordinate_y)**2)
    location.distance = distance
    return distance

@pytest.fixture
def make_locations():
    return [
        Location.objects.create(
            name=f"loc{i}",
            coordinate_x=i*10,
            coordinate_y=i*5
        )

        for i in range(10)
    ]


@pytest.fixture
def authenticator_mock(mocker):
    def mock_value(success=True):
        mocker.patch("middlewares.permissions.IsAuthenticated._is_authenticated", return_value=success)
    
    return mock_value


@pytest.fixture
def filter_neighbors():
    def neighbors(locations, x, y, d_max):
        return list(filter(lambda location: point_distance(x, y, location) <= d_max, locations))
    
    return neighbors


@pytest.fixture
def request_mock():
    return RequestMock


@pytest.fixture
def response_mock():
    return ResponseMock
