from http import HTTPStatus

import requests
from location import settings
from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    def _is_authenticated(self, request, view):
        token = request.headers.get("Authorization")

        if token != None and request.session.get("token") == token:
            return True

        response = requests.get(f"{settings.AUTHENTICATOR_URI}/auth/verify?token={token}")
        
        if response.status_code == HTTPStatus.NOT_FOUND:
            return False
        
        request.session["user"] = response.json()
        request.session["token"] = token
        return True

    def has_permission(self, request, view):
        return self._is_authenticated(request, view)

    def has_object_permission(self, request, view, obj):
        return self._is_authenticated(request, view)