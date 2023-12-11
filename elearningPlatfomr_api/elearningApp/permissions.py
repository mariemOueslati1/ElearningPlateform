from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from courseApp.models import Course

# Define groups
student_group, created = Group.objects.get_or_create(name='Student')
tutor_group, created = Group.objects.get_or_create(name='Tutor')
admin_group, created = Group.objects.get_or_create(name='Administrator')

# Define permissions
content_type = ContentType.objects.get_for_model(Course)

#Student-specific permissions
enroll_permission, created = Permission.objects.get_or_create(
    codename='can_enroll',
    name='Can enroll in courses',
    content_type=content_type,
)
submit_assignment, created = Permission.objects.get_or_create(
    codename='submit_assignment',
    name = 'Can submit to assignments',
    content_type=content_type,
)
# Tutor-specific permissions
create_manage_courses_permission, created = Permission.objects.get_or_create(
    codename='create_manage_courses',
    name='Create and manage courses',
    content_type=content_type,
)

upload_materials_permission, created = Permission.objects.get_or_create(
    codename='upload_materials',
    name='Upload course materials',
    content_type=content_type,
)

evaluate_assignments_permission, created = Permission.objects.get_or_create(
    codename='evaluate_assignments',
    name='Evaluate and provide feedback on student assignments',
    content_type=content_type,
)

initiate_voice_calls_permission, created = Permission.objects.get_or_create(
    codename='initiate_voice_calls',
    name='Initiate voice calls to mark students as absent',
    content_type=content_type,
)
