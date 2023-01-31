from rest_framework.serializers import ModelSerializer

from fields.models import Field


class FieldSerializer(ModelSerializer):
    class Meta:
        model = Field
        fields = "__all__"


class FieldRetrieveSerializer(ModelSerializer):
    class Meta:
        model = Field
        fields = ("id", "name")
