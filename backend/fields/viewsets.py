from drf_spectacular.utils import extend_schema
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from config.permissions import DirectorPermission
from fields.models import Field
from fields.serializers import FieldSerializer


@extend_schema(tags=["Направления подготовки"])
class FieldViewSet(ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, DirectorPermission]
