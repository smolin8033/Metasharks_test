from rest_framework.serializers import ModelSerializer

from groups.serializers import StudyGroupRetrieveSerializer
from users.models import User


class UserSerializer(ModelSerializer):
    """
    Админ добавляет куратора в бд через admin page.
    Куратор создает студентов-Пользователей и управляет ими
    """

    class Meta:
        model = User
        fields = ("id", "username", "password", "first_name", "last_name", "email", "gender", "role", "study_group")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserListRetrieveSerializer(ModelSerializer):
    """Сериализатор для списка студентов-Пользователей и конкретного студента-Пользователя"""

    study_group = StudyGroupRetrieveSerializer()

    class Meta:
        model = User
        fields = ("id", "username", "password", "first_name", "last_name", "email", "gender", "role", "study_group")
