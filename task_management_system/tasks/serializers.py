from django.contrib.auth.models import Group, User
from rest_framework import serializers

from .models import Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]


class TaskSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)  # Владелец — только для чтения
    shared_with = UserSerializer(many=True, read_only=True)
    shared_groups = GroupSerializer(many=True, read_only=True)
    deadline = serializers.DateTimeField(
        allow_null=True, required=False
    )  # Поле deadline доступно для записи

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "owner",
            "deadline",
            "shared_with",
            "shared_groups",
        ]
