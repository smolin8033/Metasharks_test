import pytest
from django.urls import reverse
from rest_framework import status

from subjects.models import Subject
from tests.faked_data.factories import UserFactory, FieldFactory, SubjectFactory

pytestmark = pytest.mark.django_db

class TestSubjectViewSet:
    def test_action_no_auth(self, api_client):
        data = {
            "name": "test_name"
        }

        url = reverse("subjects-list")

        response = api_client.post(url, data=data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_action_no_perms_mentor(self, api_client):
        data = {
            "name": "test_name"
        }

        mentor = UserFactory(role="M")

        url = reverse("subjects-list")

        api_client.force_authenticate(user=mentor)
        response = api_client.post(url, data=data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_action_no_perms_student(self, api_client):
        data = {
            "name": "test_name"
        }

        student = UserFactory(role="S")

        url = reverse("subjects-list")

        api_client.force_authenticate(user=student)
        response = api_client.post(url, data=data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_action_create_by_director(self, api_client):
        field = FieldFactory()

        data = {
            "name": "test_name",
            "field": field.id
        }

        url = reverse("subjects-list")

        director = UserFactory(role="D")

        assert director.role == 'D'
        assert Subject.objects.count() == 0

        api_client.force_authenticate(user=director)
        response = api_client.post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Subject.objects.count() == 1

        new_subject = Subject.objects.first()

        assert data["name"] == new_subject.name
        assert data["field"] == new_subject.field_id

    def test_action_list_subjects(self, api_client, django_assert_max_num_queries):
        field1 = FieldFactory(name="field1")
        field2 = FieldFactory(name="field2")
        field3 = FieldFactory(name="field3")

        subjects_array = []
        subject1 = SubjectFactory(field=field1, name="subject1")
        subjects_array.append(subject1)
        subject2 = SubjectFactory(field=field2, name="subject2")
        subjects_array.append(subject2)
        subject3 = SubjectFactory(field=field3, name="subject3")
        subjects_array.append(subject3)

        assert len(subjects_array) == 3

        url = reverse("subjects-list")

        director = UserFactory(
            role="D"
        )

        api_client.force_authenticate(user=director)
        with django_assert_max_num_queries(1):
            response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        json_response = response.json()
        assert len(json_response) == 3

    def test_action_retrieve_subject(self, api_client, django_assert_max_num_queries):
        subject = SubjectFactory()

        director = UserFactory(role="D")

        url = reverse("subjects-detail", kwargs={"pk": subject.pk})

        api_client.force_authenticate(user=director)
        with django_assert_max_num_queries(1):
            response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_action_delete_subject(self, api_client):
        subject = SubjectFactory()

        director = UserFactory(role="D")

        assert Subject.objects.count() == 1

        url = reverse("subjects-detail", kwargs={"pk": subject.pk})

        api_client.force_authenticate(user=director)
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Subject.objects.count() == 0

    def test_action_update_subject(self, api_client):
        field1 = FieldFactory(name="field1")
        field2 = FieldFactory(name="field2")

        subject = SubjectFactory(field=field1)

        director = UserFactory(role="D")

        assert Subject.objects.count() == 1

        data = {
            "name": "test_name",
            "field": field2.id
        }

        url = reverse("subjects-detail", kwargs={"pk": subject.pk})

        api_client.force_authenticate(user=director)
        response = api_client.patch(url, data=data)

        assert response.status_code == status.HTTP_200_OK

        assert Subject.objects.count() == 1

        updated_subject = Subject.objects.first()

        assert updated_subject.name == data["name"]
        assert updated_subject.field_id == data["field"]
