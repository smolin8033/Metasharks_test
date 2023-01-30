from drf_spectacular.utils import extend_schema
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from config.permissions import MentorPermission
from groups.models import StudyGroup
from groups.serializers import StudyGroupSerializer, StudyGroupListSerializer


@extend_schema(tags=["Учебные группы"])
class StudyGroupViewSet(ModelViewSet):
    queryset = StudyGroup.objects.all()
    serializer_class = StudyGroupSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, MentorPermission]

    def get_queryset(self):
        queryset = StudyGroup.objects.select_related("field").prefetch_related("subjects").filter(
            field=self.request.user.field
        )
        return queryset

    def get_serializer_class(self):
        serializer_class = StudyGroupSerializer
        if self.action in (self.list.__name__, self.retrieve.__name__):
            serializer_class = StudyGroupListSerializer
        return serializer_class
