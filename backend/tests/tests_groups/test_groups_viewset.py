import pytest
from django.urls import reverse
from rest_framework import status

from groups.models import StudyGroup
from tests.faked_data.factories import (
    FieldFactory,
    StudyGroupFactory,
    SubjectFactory,
    UserFactory,
)

pytestmark = pytest.mark.django_db


class TestStudyGroupViewSet:
    def test_action_no_auth(self, api_client):
        data = {"number": 10}

        url = reverse("study_groups-list")

        response = api_client.post(url, data=data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_action_no_perms_director(self, api_client):
        data = {"number": 10}

        director = UserFactory(role="D")

        url = reverse("study_groups-list")

        api_client.force_authenticate(user=director)
        response = api_client.post(url, data=data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_action_no_perms_student(self, api_client):
        data = {"number": 10}

        student = UserFactory(role="S")

        url = reverse("study_groups-list")

        api_client.force_authenticate(user=student)
        response = api_client.post(url, data=data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_action_create_by_mentor(self, api_client):
        data = {"number": 10}

        url = reverse("study_groups-list")

        mentor = UserFactory(role="M")

        assert mentor.role == "M"
        assert StudyGroup.objects.count() == 1

        api_client.force_authenticate(user=mentor)
        response = api_client.post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert StudyGroup.objects.count() == 2

        new_group = StudyGroup.objects.all()[1]

        assert data["number"] == new_group.number

    def test_action_list_groups(self, api_client, django_assert_max_num_queries):
        field = FieldFactory()

        subject1 = SubjectFactory(field=field, name="subject1")
        subject2 = SubjectFactory(field=field, name="subject2")

        groups_array = []
        group1 = StudyGroupFactory(field=field, number=11, subjects=(subject1, subject2))
        groups_array.append(group1)
        group2 = StudyGroupFactory(field=field, number=12, subjects=(subject1, subject2))
        groups_array.append(group2)
        group3 = StudyGroupFactory(field=field, number=13, subjects=(subject1, subject2))
        groups_array.append(group3)
        group4 = StudyGroupFactory(field=field, number=14, subjects=(subject1, subject2))
        groups_array.append(group4)

        assert len(groups_array) == 4

        url = reverse("study_groups-list")

        mentor = UserFactory(role="M", field=field, study_group=None)

        api_client.force_authenticate(user=mentor)
        with django_assert_max_num_queries(3):
            response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        json_response = response.json()
        assert len(json_response) == 4

    def test_action_retrieve_group(self, api_client, django_assert_max_num_queries):
        field = FieldFactory()
        group = StudyGroupFactory(field=field)

        mentor = UserFactory(username="mentor", role="M", field=field)

        url = reverse("study_groups-detail", kwargs={"pk": group.pk})

        api_client.force_authenticate(user=mentor)
        with django_assert_max_num_queries(3):
            response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_action_delete_group(self, api_client):
        field = FieldFactory()
        group = StudyGroupFactory(field=field)

        mentor = UserFactory(username="mentor", role="M", field=field, study_group=None)

        assert StudyGroup.objects.count() == 1

        url = reverse("study_groups-detail", kwargs={"pk": group.pk})

        api_client.force_authenticate(user=mentor)
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert StudyGroup.objects.count() == 0

    def test_action_update_group(self, api_client):
        field1 = FieldFactory(name="field1")
        field2 = FieldFactory(name="field2")

        group = StudyGroupFactory(field=field1)

        mentor = UserFactory(username="mentor", role="M", field=field1, study_group=None)

        assert StudyGroup.objects.count() == 1

        data = {"number": 25, "field": field2.id}

        url = reverse("study_groups-detail", kwargs={"pk": group.pk})

        api_client.force_authenticate(user=mentor)
        response = api_client.patch(url, data=data)

        assert response.status_code == status.HTTP_200_OK

        assert StudyGroup.objects.count() == 1

        updated_group = StudyGroup.objects.first()

        assert updated_group.number == data["number"]
        assert updated_group.field == field2
