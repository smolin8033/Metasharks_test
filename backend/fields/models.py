from django.db import models


class Field(models.Model):
    """
    Направления подготовки. За каждым закреплен один куратор. У них множество учебных дисциплин.
    """
    name = models.CharField(max_length=40, unique=True, blank=False, null=False)
