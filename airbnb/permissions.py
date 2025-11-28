from rest_framework.permissions import BasePermission

class CheckReview(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'guest'

class CreateProperty(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'host'