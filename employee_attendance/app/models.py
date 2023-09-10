from django.db import models
from django.utils import timezone

class User(models.Model):
    username = models.CharField(max_length=255)
    pin = models.CharField(max_length=4)
    hourly_wage = models.IntegerField()

class WeekSchedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='week_schedules')
    day_of_week = models.IntegerField(choices=(
        (0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'),
        (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')
    ))
    start_time = models.TimeField()

class ClockEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clock_entries')
    clock_in = models.DateTimeField()
    clock_out = models.DateTimeField(null=True, blank=True)
    wage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    late_minutes = models.IntegerField(default=0)  # New field to store late minutes
    minuts_worked = models.IntegerField(default=0)

   
