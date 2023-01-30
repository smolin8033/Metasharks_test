from rest_framework.routers import DefaultRouter

from .viewsets import SubjectViewSet

router = DefaultRouter()
router.register("subjects", SubjectViewSet, basename="subjects")
