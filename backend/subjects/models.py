from django.db import models

from fields.models import Field


class Subject(models.Model):
    """
    Учебные дисциплины. У них может быть одно направление подготовки и много групп.
    """
    name = models.CharField(max_length=30, blank=False, null=False)
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='subjects', blank=True, null=True)
