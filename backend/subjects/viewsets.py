from drf_spectacular.utils import extend_schema
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from config.permissions import DirectorPermission
from subjects.models import Subject
from subjects.serializers import SubjectSerializer, SubjectListSerializer


@extend_schema(tags=["Учебные дисциплины"])
class SubjectViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, DirectorPermission]

    def get_queryset(self):
        queryset = Subject.objects.select_related("field")
        return queryset

    def get_serializer_class(self):
        serializer_class = SubjectSerializer
        if self.action in (self.list.__name__, self.retrieve.__name__):
            serializer_class = SubjectListSerializer
        return serializer_class
