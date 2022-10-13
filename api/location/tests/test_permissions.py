import pytest
from middlewares.permissions import IsAuthenticated
from location import settings

class TestIsAuthenticated:
    def test__is_authenticated(self, mocker, request_mock, response_mock):
        request = request_mock(headers={"Authorization": "48309809384349089023"}, session={})
        response = response_mock(status_code=200)
        mock_get = mocker.patch("requests.get", return_value=response)

        result = IsAuthenticated()._is_authenticated(request, {})

        mock_get.assert_called_with(f"{settings.AUTHENTICATOR_URI}/auth/verify?token={request.headers['Authorization']}")
        assert result
        assert request.session.get("token") == request.headers['Authorization']
        assert request.session.get("user") == {}
    
    def test__is_authenticated_token_already_exists(self, mocker, request_mock):
        request = request_mock(headers={"Authorization": "48309809384349089023"}, session={"token": "48309809384349089023"})
        mock_get = mocker.patch("requests.get")

        result = IsAuthenticated()._is_authenticated(request, {})

        mock_get.assert_not_called()
        assert result
    
    def test_not_is_authenticated(self, mocker, request_mock, response_mock):
        request = request_mock(headers={"Authorization": "48309809384349089023"}, session={})
        response = response_mock(status_code=404)
        mock_get = mocker.patch("requests.get", return_value=response)

        result = IsAuthenticated()._is_authenticated(request, {})

        mock_get.assert_called_with(f"{settings.AUTHENTICATOR_URI}/auth/verify?token={request.headers['Authorization']}")
        assert not result
        assert request.session.get("token") == None
        assert request.session.get("user") == None
    
    @pytest.mark.parametrize(
        "permited",
        [
            True,
            False
        ]
    )
    def test_has_permission(self, mocker, permited):
        mock_is_authenticated = mocker.patch.object(IsAuthenticated, '_is_authenticated', return_value=permited)

        result = IsAuthenticated().has_permission({}, {})

        mock_is_authenticated.assert_called_with({}, {})
        assert result == permited
    
    @pytest.mark.parametrize(
        "permited",
        [
            True,
            False
        ]
    )
    def test_has_object_permission(self, mocker, permited):
        mock_is_authenticated = mocker.patch.object(IsAuthenticated, '_is_authenticated', return_value=permited)

        result = IsAuthenticated().has_object_permission({}, {}, {})

        mock_is_authenticated.assert_called_with({}, {})
        assert result == permited

        