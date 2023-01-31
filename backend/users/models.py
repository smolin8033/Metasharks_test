from django.contrib.auth.models import AbstractUser, UserManager
from django.db import IntegrityError, models

from fields.models import Field
from groups.models import StudyGroup
from users.constants import GENDER_CHOICES, ROLE_CHOICES
from users.validators import restrict_number


class User(AbstractUser):
    """
    Пользователь. Может быть либо куратором, либо студентом, либо администратором(админ)
    """

    role = models.CharField(max_length=30, blank=True, choices=ROLE_CHOICES)
    gender = models.CharField(max_length=10, blank=True, choices=GENDER_CHOICES)
    field = models.OneToOneField(Field, on_delete=models.CASCADE, blank=True, null=True, related_name="supervisors")
    study_group = models.ForeignKey(
        StudyGroup,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="students",
        validators=(restrict_number,),
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["password"]

    objects = UserManager()

    def __str__(self):
        return f"Role: {self.role}. Username {self.username}. Name: {self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if self.study_group:
            if self.study_group.count_students < 20:
                super().save(*args, **kwargs)
                self.study_group.count_students += 1
                self.study_group.save()
            else:
                raise IntegrityError("A study group can't have more than 20 students")
        else:
            super().save(*args, **kwargs)
