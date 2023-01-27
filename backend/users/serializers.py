from rest_framework.serializers import ModelSerializer

from users.models import User


class UserCreateSerializer(ModelSerializer):
    """Сериализация для создания Пользователя"""
    class Meta:
        model = User
        fields = (

        )
