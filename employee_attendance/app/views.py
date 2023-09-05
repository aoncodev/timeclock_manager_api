from rest_framework import generics
from .models import User, ClockEntry
from .serializers import UserSerializer, ClockEntrySerializer

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ClockEntryListCreateView(generics.ListCreateAPIView):
    queryset = ClockEntry.objects.all()
    serializer_class = ClockEntrySerializer

class ClockEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClockEntry.objects.all()
    serializer_class = ClockEntrySerializer
