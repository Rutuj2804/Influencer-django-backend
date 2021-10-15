from rest_framework import serializers
from .models import TimeSpend


class TimeSpendSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSpend
        fields = '__all__'
        depth = 1