from rest_framework import permissions
class evaluate_assignments_permission(permissions.BasePermission):
    message = "You do not have permission to evaluate assignments"

    def has_permission(self, request, view):
        return request.user and request.user.has_perm('courseApp.evaluate_assignments')