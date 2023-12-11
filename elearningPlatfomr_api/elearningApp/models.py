from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth import get_user_model


class UserProfile(AbstractUser):
    role_choicesList = [('Student', 'Student'), ('Tutor', 'Tutor')]
    roleList = models.CharField(max_length=15, choices=role_choicesList, default='Student')
    
    groups = models.ManyToManyField(Group, related_name='user_profiles')
    user_permissions = models.ManyToManyField(Permission, related_name='user_profiles')

    def save(self, *args, **kwargs):
        from .permissions import student_group, tutor_group, admin_group, enroll_permission,create_manage_courses_permission,upload_materials_permission,evaluate_assignments_permission,initiate_voice_calls_permission, submit_assignment
        super().save(*args, **kwargs)

        if self.roleList == 'Student':
            self.groups.add(student_group)
            self.user_permissions.add(
                enroll_permission,
                submit_assignment)
            
        elif self.roleList == 'Tutor':
            self.groups.add(tutor_group)
            self.user_permissions.add(
                create_manage_courses_permission,
                upload_materials_permission,
                evaluate_assignments_permission,
                initiate_voice_calls_permission,
            )
        
            

    def __str__(self):
        return self.username

