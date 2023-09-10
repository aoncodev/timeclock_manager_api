from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserListCreateAPIView.as_view(), name='user-list-create'),
    path('users/<int:user_id>/', views.UserListCreateAPIView.as_view(), name='user-delete'),
    path('user/<int:user_id>/', views.UserDetailAPIView.as_view(), name='user-detail'),
    path('users/update/<int:pk>/', views.UserRetrieveUpdateAPIView.as_view(), name='user-update'),
    path('update/week/<int:pk>/', views.WeekScheduleUpdateAPIView.as_view(), name='week-schedule-update'),
    path('clock/', views.ClockEntryAPIView.as_view(), name='clockentry-list-create'),
    path('date/<str:date>/', views.UserClockDataAPIView.as_view(), name='user-clock-data'),
]
