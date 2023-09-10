from rest_framework import serializers
from .models import User, WeekSchedule, ClockEntry

class WeekScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeekSchedule
        fields = '__all__'




class ClockEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClockEntry
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    week_schedules = WeekScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'


class UserClockDataSerializer(serializers.Serializer):
    user_id  = serializers.IntegerField()
    username = serializers.CharField()
    wage = serializers.IntegerField()
    minutes_worked = serializers.CharField()
    late = serializers.IntegerField()
    first_clock_in = serializers.DateTimeField()
    last_clock_out = serializers.DateTimeField()