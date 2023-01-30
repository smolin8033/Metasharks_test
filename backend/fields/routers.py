from rest_framework.routers import DefaultRouter

from .viewsets import FieldViewSet

router = DefaultRouter()
router.register("fields", FieldViewSet, basename="fields")
