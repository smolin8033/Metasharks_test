from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer


@extend_schema(tags=["Пользователи"])
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
