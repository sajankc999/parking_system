from rest_framework.permissions import SAFE_METHODS, BasePermission

"""

Permission Class for customer

"""


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.customer


"""
Class for Employee permission

"""


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.employee


"""
Class for SuperUser permission

"""


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
