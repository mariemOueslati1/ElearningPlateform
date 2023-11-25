from rest_framework import permissions

class enroll_permission(permissions.BasePermission):
    message = 'You do not have permission to enroll the course.'

    def has_permission(self, request, view):
        # Check if the user has permission to view enrollments
        return request.user.has_perm('courseApp.can_enroll')

class IsEnrollmentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the authenticated user is the owner of the enrollment
        return obj.student == request.user