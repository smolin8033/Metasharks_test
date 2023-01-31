from django.contrib import admin

from subjects.models import Subject


@admin.register(Subject)
class Subject(admin.ModelAdmin):
    pass
