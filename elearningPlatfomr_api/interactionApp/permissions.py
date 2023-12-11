from rest_framework import permissions

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated and is a student
        return request.user.is_authenticated and request.user.roleList == 'Student'