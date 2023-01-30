from rest_framework.serializers import ModelSerializer

from fields.serializers import FieldRetrieveSerializer
from subjects.models import Subject


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class SubjectRetrieveSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'name')


class SubjectListSerializer(ModelSerializer):
    field = FieldRetrieveSerializer()

    class Meta:
        model = Subject
        fields = ('id', 'name', 'field')
