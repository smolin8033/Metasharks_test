from drf_spectacular.utils import extend_schema
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from config.permissions import MentorPermission
from users.models import User
from users.serializers import UserListRetrieveSerializer, UserSerializer

# TODO action add student

# TODO constraint
# TODO test constraint max 20

# TODO celery + queries + excel
# TODO endpoint
# TODO celery tests

# TODO mypy

# TODO final linting


@extend_schema(tags=["Пользователи"])
class UserViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, MentorPermission]

    def get_queryset(self):
        queryset = User.objects.select_related("study_group", "field").filter(
            study_group__field=self.request.user.field
        )
        return queryset

    def get_serializer_class(self):
        serializer_class = UserSerializer
        if self.action in (self.list.__name__, self.retrieve.__name__):
            serializer_class = UserListRetrieveSerializer
        return serializer_class
