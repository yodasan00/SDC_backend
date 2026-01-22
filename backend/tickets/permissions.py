from rest_framework.permissions import BasePermission

class IsDepartmentUser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'DEPARTMENT'
        )

class IsDITUser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'DIT'
        )

class IsSDCUser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'SDC'
        )
<<<<<<< Updated upstream

=======
    
    
>>>>>>> Stashed changes
class IsOfficer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'OFFICER'