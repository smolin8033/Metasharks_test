# flake8: noqa
from django.core.exceptions import ValidationError


def restrict_number(value):
    if User.objects.filter(study_group=value).count() > 20:
        raise ValidationError("Группа переполнена. В ней максимальное количество студентов (20)")
