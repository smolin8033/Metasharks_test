from django.db import models


class Field(models.Model):
    """
    Направление подготовки.
    За каждым закреплен один куратор.
    У него множество учебных дисциплин.
    К нему прикреплено множество учебных групп.
    """
    name = models.CharField(max_length=40, unique=True, blank=False, null=False)

    def __str__(self):
        return self.name
