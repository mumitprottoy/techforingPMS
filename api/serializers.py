from rest_framework import serializers
from pms import models


class UserSerializer(serializers.ModelSerializer):
    """
    The user password is write only
    """
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = models.User
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = '__all__'


class ProjectMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectMember
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = '__all__'