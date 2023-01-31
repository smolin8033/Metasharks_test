from rest_framework.routers import DefaultRouter

from .viewsets import ReportViewSet, UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("report", ReportViewSet, basename="report")
