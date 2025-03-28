from rest_framework import serializers
from todo.models import ToDo


class ToDoSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()
    completed = serializers.ReadOnlyField()
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ToDo
        fields = ['id', 'title', 'memo', 'created', 'completed', 'user']


class ToDoToggleCompleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = ToDo
        fields = ['title', 'memo', 'created', 'completed']
