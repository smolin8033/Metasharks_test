from rest_framework.permissions import BasePermission


class MentorPermission(BasePermission):
    """Пермишионы для куратора"""
    def has_permission(self, request, view):
        if request.user.role == 'M':
            return True


class DirectorPermission(BasePermission):
    """Пермишионы для администратора"""
    def has_permission(self, request, view):
        if request.user.role == 'D':
            return True
