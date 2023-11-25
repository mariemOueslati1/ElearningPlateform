from rest_framework import permissions
class CanUpsubmitAssignment(permissions.BasePermission):
    message = "You do not have permission to submit assignments"

    def has_permission(self, request, view):
        return request.user and request.user.has_perm('courseApp.submit_assignment')