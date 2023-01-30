from django.db import models

from fields.models import Field
from subjects.models import Subject


class StudyGroup(models.Model):
    """
    Группы. В них могут быть многие студенты, у них может быть множество учебных дисциплин
    """
    number = models.IntegerField(unique=True, null=False, blank=False)
    subjects = models.ManyToManyField(Subject, blank=True)
    field = models.ForeignKey(Field, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number)
