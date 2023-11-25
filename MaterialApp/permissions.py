from rest_framework import permissions
class CanUploadMaterialPermission(permissions.BasePermission):
    message = "You do not have permission to upload materials."

    def has_permission(self, request, view):
        return request.user and request.user.has_perm('courseApp.upload_materials')

class IsCourseTutor(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is the tutor of the course
        course = view.get_course(view.kwargs.get('course_id'))
        return request.user == course.tutor

    def has_object_permission(self, request, view, obj):
        # Ensure that the user is the tutor when dealing with object-level permissions
        return request.user == obj.course.tutor

