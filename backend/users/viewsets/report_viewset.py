from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from common.mixins.permissions import DirectorPermission
from users.tasks import start_report_generation


@extend_schema(tags=["Отчет администратора"])
class ReportViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated, DirectorPermission]

    @action(detail=False)
    def run_report(self, request):
        start_report_generation.delay()
        return Response({"status": "ok"})
