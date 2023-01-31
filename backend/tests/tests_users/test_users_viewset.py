import pytest
from django.db import IntegrityError
from django.urls import reverse
from rest_framework import status

from groups.models import StudyGroup
from tests.faked_data.factories import FieldFactory, StudyGroupFactory, UserFactory
from users.models import User

pytestmark = pytest.mark.django_db


class TestUserViewSet:
    def test_action_no_auth(self, api_client):
        data = {
            "username": "test_username",
            "password": "test_password",
        }

        url = reverse("users-list")

        response = api_client.post(url, data=data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_action_no_perms_director(self, api_client):
        data = {
            "username": "test_username",
            "password": "test_password",
        }

        user = UserFactory()
        user.role = "D"

        url = reverse("users-list")

        api_client.force_authenticate(user=user)
        response = api_client.post(url, data=data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_action_no_perms_student(self, api_client):
        data = {
            "username": "test_username",
            "password": "test_password",
        }

        user = UserFactory()
        user.role = "S"

        url = reverse("users-list")

        api_client.force_authenticate(user=user)
        response = api_client.post(url, data=data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_action_create_by_mentor(self, api_client):
        data = {
            "username": "test_username",
            "password": "test_password",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "email": "test@mail.ru",
            "gender": "M",
            "role": "S",
        }

        url = reverse("users-list")

        user = UserFactory()
        user.role = "M"

        assert user.role == "M"

        api_client.force_authenticate(user=user)
        response = api_client.post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert len(User.objects.all()) == 2

        new_user = User.objects.get(username="test_username")

        assert data["first_name"] == new_user.first_name
        assert data["last_name"] == new_user.last_name
        assert data["email"] == new_user.email
        assert data["gender"] == new_user.gender
        assert data["role"] == new_user.role

    def test_action_list_students(self, api_client, django_assert_max_num_queries):
        field = FieldFactory()
        group = StudyGroupFactory(field=field)
        assert len(StudyGroup.objects.all()) == 1

        users_array = []
        user1 = UserFactory(study_group=group, username="user1")
        users_array.append(user1)
        user2 = UserFactory(study_group=group, username="user2")
        users_array.append(user2)
        user3 = UserFactory(study_group=group, username="user3")
        users_array.append(user3)
        user4 = UserFactory(study_group=group, username="user4")
        users_array.append(user4)

        assert len(users_array) == 4

        url = reverse("users-list")

        user = UserFactory(role="M", field=field, study_group=None)

        api_client.force_authenticate(user=user)
        with django_assert_max_num_queries(3):
            response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        json_response = response.json()
        assert len(json_response) == 4

    def test_constraint_with_20_students(self, api_client, django_assert_max_num_queries):
        field = FieldFactory()
        group = StudyGroupFactory(field=field)
        users_array = []
        for i in range(20):
            users_array.append(UserFactory(study_group=group, username=f"username{i}"))

        assert users_array[0].study_group == group
        assert users_array[1].study_group == group
        assert len(users_array) == 20

    def test_constraint_more_20_students(self, api_client, django_assert_max_num_queries):
        field = FieldFactory()
        group = StudyGroupFactory(field=field)
        users_array = []
        for i in range(20):
            users_array.append(UserFactory(study_group=group, username=f"username{i}"))

        with pytest.raises(IntegrityError):
            users_array.append(UserFactory(study_group=group, username="test_username"))

    def test_action_retrieve_student(self, api_client, django_assert_max_num_queries):
        field = FieldFactory()
        group = StudyGroupFactory(field=field)

        mentor = UserFactory(username="mentor", role="M", field=field)

        student = UserFactory(username="student", role="S", study_group=group)

        url = reverse("users-detail", kwargs={"pk": student.pk})

        api_client.force_authenticate(user=mentor)
        with django_assert_max_num_queries(3):
            response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_action_delete_student(self, api_client):
        field = FieldFactory()
        group = StudyGroupFactory(field=field)

        mentor = UserFactory(username="mentor", role="M", field=field)

        student = UserFactory(username="student", role="S", study_group=group)

        assert User.objects.count() == 2

        url = reverse("users-detail", kwargs={"pk": student.pk})

        api_client.force_authenticate(user=mentor)
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert User.objects.count() == 1

    def test_action_update(self, api_client):
        field = FieldFactory()
        group = StudyGroupFactory(field=field)

        mentor = UserFactory(username="mentor", role="M", field=field)

        student = UserFactory(username="student", role="S", study_group=group)

        assert User.objects.count() == 2

        data = {
            "username": "test_username",
            "password": "test_password",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "email": "test@mail.ru",
            "gender": "M",
            "role": "S",
        }

        url = reverse("users-detail", kwargs={"pk": student.pk})

        api_client.force_authenticate(user=mentor)
        response = api_client.patch(url, data=data)

        assert response.status_code == status.HTTP_200_OK

        assert User.objects.count() == 2

        updated_student = User.objects.get(role="S")

        assert updated_student.username == data["username"]
        assert updated_student.first_name == data["first_name"]
        assert updated_student.last_name == data["last_name"]
        assert updated_student.email == data["email"]
        assert updated_student.gender == data["gender"]
        assert updated_student.role == data["role"]
