from django.db import models
from django.db.models import Q

from fields.models import Field
from subjects.models import Subject
from users.constants import MAX_STUDENTS_NUMBER


class StudyGroup(models.Model):
    """
    Группы. В них могут быть многие студенты, у них может быть множество учебных дисциплин
    """

    number = models.IntegerField(unique=True, null=False, blank=False)
    subjects = models.ManyToManyField(Subject, blank=True)
    field = models.ForeignKey(Field, blank=True, null=True, on_delete=models.CASCADE)
    count_students = models.IntegerField(default=0)

    class Meta:
        constraints = [models.CheckConstraint(check=Q(count_students__lte=MAX_STUDENTS_NUMBER), name="students_lte_20")]

    def __str__(self):
        return str(self.number)
