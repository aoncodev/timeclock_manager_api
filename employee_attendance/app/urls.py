from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserListCreateAPIView.as_view(), name='user-list-create'),
    path('clock-entries/', views.ClockEntryListCreateAPIView.as_view(), name='clockentry-list-create'),
    path('clock-in-out/', views.ClockEntryAPIView.as_view(), name='clock-in-out'),
    path('clock-entries/<int:pk>/', views.ClockEntryDetailAPIView.as_view(), name='clockentry-detail'),
]
