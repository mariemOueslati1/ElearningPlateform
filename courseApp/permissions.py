from rest_framework import permissions
class CanUpdateCoursePermission(permissions.BasePermission):
    message = 'You do not have permission to update this course.'

    def has_permission(self, request, view):
        return request.user and request.user.has_perm('courseApp.create_manage_courses')

class CanDeleteCoursePermission(permissions.BasePermission):
    message = 'You do not have permission to delete this course.'

    def has_object_permission(self, request, view, obj):
        # Check if the user has permission to delete the course and if the user is the tutor of the course
        return request.user.has_perm('courseApp.create_manage_courses') and obj.tutor == request.user