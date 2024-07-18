from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return  request.user.customer 
    
class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return  request.user.employee
    
class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return  request.user.is_superuser
        