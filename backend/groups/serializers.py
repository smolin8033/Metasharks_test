from rest_framework.serializers import ModelSerializer

from fields.serializers import FieldRetrieveSerializer
from groups.models import StudyGroup
from subjects.serializers import SubjectRetrieveSerializer


class StudyGroupRetrieveSerializer(ModelSerializer):
    class Meta:
        model = StudyGroup
        fields = ("id", "number")


class StudyGroupSerializer(ModelSerializer):
    class Meta:
        model = StudyGroup
        fields = "__all__"


class StudyGroupListSerializer(ModelSerializer):
    subjects = SubjectRetrieveSerializer(many=True)
    field = FieldRetrieveSerializer()

    class Meta:
        model = StudyGroup
        fields = ("id", "number", "subjects", "field")
