from django.contrib import admin

from groups.models import StudyGroup


@admin.register(StudyGroup)
class StudyGroup(admin.ModelAdmin):
    pass