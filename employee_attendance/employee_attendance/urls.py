from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('clock_in_out.urls')),
]
