# flake8: noqa

import pytest
from django.urls import reverse
from rest_framework import status

from fields.models import Field
from subjects.models import Subject
from tests.faked_data.factories import FieldFactory, SubjectFactory, UserFactory

pytestmark = pytest.mark.django_db


class TestFieldViewSet:
    def test_action_no_auth(self, api_client):
        data = {"name": "test_name"}

        url = reverse("fields-list")

        response = api_client.post(url, data=data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_action_no_perms_mentor(self, api_client):
        data = {"name": "test_name"}

        mentor = UserFactory(role="M")

        url = reverse("fields-list")

        api_client.force_authenticate(user=mentor)
        response = api_client.post(url, data=data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_action_no_perms_student(self, api_client):
        data = {"name": "test_name"}

        student = UserFactory(role="S")

        url = reverse("fields-list")

        api_client.force_authenticate(user=student)
        response = api_client.post(url, data=data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_action_create_by_director(self, api_client):
        data = {"name": "test_name"}

        url = reverse("fields-list")

        director = UserFactory(role="D")

        assert director.role == "D"
        assert Field.objects.count() == 1

        api_client.force_authenticate(user=director)
        response = api_client.post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Field.objects.count() == 2

        new_field = Field.objects.all()[1]

        assert data["name"] == new_field.name

    def test_action_list_fields(self, api_client, django_assert_max_num_queries):
        fields_array = []
        field1 = FieldFactory(name="field1")
        fields_array.append(field1)
        field2 = FieldFactory(name="field2")
        fields_array.append(field2)
        field3 = FieldFactory(name="field3")
        fields_array.append(field3)
        field4 = FieldFactory(name="field4")
        fields_array.append(field4)

        assert len(fields_array) == 4

        url = reverse("fields-list")

        director = UserFactory(role="D", field=None, study_group=None)

        api_client.force_authenticate(user=director)
        with django_assert_max_num_queries(1):
            response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        json_response = response.json()
        assert len(json_response) == 4

    def test_action_retrieve_field(self, api_client, django_assert_max_num_queries):
        field = FieldFactory()

        director = UserFactory(role="D")

        url = reverse("fields-detail", kwargs={"pk": field.pk})

        api_client.force_authenticate(user=director)
        with django_assert_max_num_queries(1):
            response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_action_delete_field(self, api_client):
        subject = SubjectFactory()

        director = UserFactory(role="D")

        assert Field.objects.count() == 1

        field = Field.objects.first()

        url = reverse("fields-detail", kwargs={"pk": field.pk})

        api_client.force_authenticate(user=director)
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Field.objects.count() == 0
        assert Subject.objects.count() == 0

    def test_action_update_field(self, api_client):
        field = FieldFactory()

        director = UserFactory(role="D")

        assert Field.objects.count() == 1

        data = {"name": "test_name"}

        url = reverse("fields-detail", kwargs={"pk": field.pk})

        api_client.force_authenticate(user=director)
        response = api_client.patch(url, data=data)

        assert response.status_code == status.HTTP_200_OK

        assert Field.objects.count() == 1

        updated_field = Field.objects.first()

        assert updated_field.name == data["name"]
