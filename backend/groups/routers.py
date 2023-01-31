from rest_framework.routers import DefaultRouter

from .viewsets import StudyGroupViewSet

router = DefaultRouter()
router.register("study_groups", StudyGroupViewSet, basename="study_groups")
