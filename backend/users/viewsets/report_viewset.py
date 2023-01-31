from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from users.tasks import start_report_generation


class ReportViewSet(GenericViewSet):
    @action(detail=False)
    def run_report(self, request):
        start_report_generation.delay()
        return Response({"status": "ok"})
