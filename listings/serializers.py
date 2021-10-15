from .models import Project, Reward, WorkDescription
from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        depth = 2


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = '__all__'
        depth = 2


class WrokDescSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkDescription
        fields = '__all__'
        depth = 2


class ProjectShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'created_at', 'type', 'place', 'payment', 'completed', 'deleted', 'completed', 'positions', 'user', 'applications', 'requirements']
        depth = 2