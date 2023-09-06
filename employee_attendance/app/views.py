from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as http_status
from .serializers import UserSerializer, ClockEntrySerializer,  User, ClockEntry
from django.utils import timezone
from decimal import Decimal  # Import Decimal


from django.utils import timezone
from decimal import Decimal
from rest_framework.response import Response
from rest_framework import status as http_status
from rest_framework.views import APIView
from .models import User, ClockEntry

class ClockEntryAPIView(APIView):
    def post(self, request):
        pin = request.data.get('pin')
        status = request.data.get('status')

        if not pin:
            return Response({'message': 'PIN is required'}, status=http_status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pin=pin)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=http_status.HTTP_404_NOT_FOUND)

        response_data = {}  # Create a dictionary to hold response data

        if status == "true":
            # Clock in the user
            existing_clock_entry = ClockEntry.objects.filter(user=user, clock_out__isnull=True).first()
            if existing_clock_entry:
                return Response({'message': f'{user.username} is already clocked in'}, status=http_status.HTTP_400_BAD_REQUEST)
            
            clock_entry = ClockEntry.objects.create(user=user, clock_in=timezone.now())
            response_data['message'] = 'Clock in successful'
            response_data['user'] = user.username
            response_data['clock_in_time'] = clock_entry.clock_in
            return Response(response_data, status=http_status.HTTP_201_CREATED)
        else:
            # Clock out the user
            try:
                last_clock_entry = ClockEntry.objects.filter(user=user, clock_out__isnull=True).latest('clock_in')
                last_clock_entry.clock_out = timezone.now()
                # Calculate wages (convert hours_worked to Decimal)
                hourly_wage = user.hourly_wage
                clock_in_time = last_clock_entry.clock_in
                clock_out_time = last_clock_entry.clock_out
                hours_worked = (clock_out_time - clock_in_time).total_seconds() / 3600.0
                hours_worked_decimal = Decimal(hours_worked)  # Convert to Decimal
                last_clock_entry.wage = hourly_wage * hours_worked_decimal  # Perform multiplication
                last_clock_entry.save()
                
                response_data['message'] = 'Clock out successful'
                response_data['user'] = user.username
                response_data['clock_in_time'] = clock_in_time
                response_data['clock_out_time'] = clock_out_time
                return Response(response_data, status=http_status.HTTP_200_OK)
            except ClockEntry.DoesNotExist:
                return Response({'message': 'Clock in before clocking out'}, status=http_status.HTTP_400_BAD_REQUEST)

            
class UserListCreateAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=http_status.HTTP_201_CREATED)
        return Response(serializer.errors, status=http_status.HTTP_400_BAD_REQUEST)

class ClockEntryListCreateAPIView(APIView):
    def get(self, request):
        clock_entries = ClockEntry.objects.all()
        serializer = ClockEntrySerializer(clock_entries, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClockEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=http_status.HTTP_201_CREATED)
        return Response(serializer.errors, status=http_status.HTTP_400_BAD_REQUEST)

class ClockEntryDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            clock_entry = ClockEntry.objects.get(pk=pk)
        except ClockEntry.DoesNotExist:
            return Response(status=http_status.HTTP_404_NOT_FOUND)

        serializer = ClockEntrySerializer(clock_entry)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            clock_entry = ClockEntry.objects.get(pk=pk)
        except ClockEntry.DoesNotExist:
            return Response(status=http_status.HTTP_404_NOT_FOUND)

        serializer = ClockEntrySerializer(clock_entry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=http_status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            clock_entry = ClockEntry.objects.get(pk=pk)
        except ClockEntry.DoesNotExist:
            return Response(status=http_status.HTTP_404_NOT_FOUND)

        clock_entry.delete()
        return Response(status=http_status.HTTP_204_NO_CONTENT)
