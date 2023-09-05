from django.db import models


class User(models.Model):
    username = models.CharField(max_length=255)
    pin = models.CharField(max_length=4)
    hourly_wage = models.DecimalField(max_digits=10, decimal_places=2)

class ClockEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    clock_in = models.DateTimeField()
    clock_out = models.DateTimeField(null=True, blank=True)
    wage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
