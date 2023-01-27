from django.contrib import admin

from fields.models import Field


@admin.register(Field)
class Field(admin.ModelAdmin):
    pass
