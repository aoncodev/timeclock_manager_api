from rest_framework import serializers
from .models import User, ClockEntry

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ClockEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClockEntry
        fields = '__all__'
