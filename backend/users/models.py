from django.contrib.auth.models import AbstractUser
from django.db import models

from fields.models import Field
from groups.models import StudyGroup
from users.constants import ROLE_CHOICES, GENDER_CHOICES


class User(AbstractUser):
    """
    Пользователь. Может быть либо куратором, либо студентом, либо администратором(админ)
    """
    role = models.CharField(max_length=30, blank=True, choices=ROLE_CHOICES)
    gender = models.CharField(max_length=10, blank=True, choices=GENDER_CHOICES)
    field = models.OneToOneField(Field, on_delete=models.CASCADE, blank=True, null=True, related_name="supervisors")
    study_group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, blank=True, null=True, related_name="students")

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["password"]
