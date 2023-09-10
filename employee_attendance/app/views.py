from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as http_status
from .serializers import UserSerializer,  User, ClockEntry, WeekScheduleSerializer, ClockEntrySerializer, UserClockDataSerializer
from django.utils import timezone
from decimal import Decimal  # Import Decimal


from django.utils import timezone
from decimal import Decimal
from rest_framework.response import Response
from rest_framework import status as http_status
from rest_framework.views import APIView
from .models import User, ClockEntry, WeekSchedule
from rest_framework.generics import RetrieveUpdateAPIView, UpdateAPIView
from datetime import datetime, time
from django.db.models import Sum, Min, Max
import math

class WeekScheduleUpdateAPIView(RetrieveUpdateAPIView):
    queryset = WeekSchedule.objects.all()
    serializer_class = WeekScheduleSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(f"Updating WeekSchedule with ID: {instance.id}")
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        print(f"Updated WeekSchedule with ID: {instance.id}")
        return Response(serializer.data)



class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class ClockEntryAPIView(APIView):
    def get(self, request):
        # Retrieve a list of users
        clockEntry = ClockEntry.objects.all()
        serializer = ClockEntrySerializer(clockEntry, many=True)
        return Response(serializer.data)
    
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
            
            # Check for late clock-in
            
            schedule = WeekSchedule.objects.filter(user=user, day_of_week=timezone.localtime(timezone.now()).weekday()).first()
            if schedule:
                current_time = timezone.localtime(timezone.now())
                print(f"current: {current_time}")
                print(schedule.start_time)
                schedule_start_time = schedule.start_time

                # Extract the hour and minute components
                start_hour = schedule_start_time.hour
                start_minute = schedule_start_time.minute

                # Create a new datetime with custom second value (0)
                custom_datetime = current_time.replace(hour=start_hour, minute=start_minute, second=0)
                print(f"Custom datetime: {custom_datetime}")
                # Get the current time in your desired time zone
                

                
                time_difference_seconds = (current_time - custom_datetime).total_seconds()
                time_difference_minutes = time_difference_seconds / 60

                
                late_minutes = max(0, math.floor(time_difference_minutes))
                
                clock_entry = ClockEntry.objects.create(user=user, clock_in=current_time, late_minutes=late_minutes)
            else:
                # No schedule found for the day, clock in without checking for lateness
                clock_entry = ClockEntry.objects.create(user=user, clock_in=timezone.now())

            response_data['message'] = 'Clock in successful'
            response_data['user'] = user.username
            response_data['clock_in_time'] = clock_entry.clock_in
            response_data['late'] = clock_entry.late_minutes
            return Response(response_data, status=http_status.HTTP_201_CREATED)
        else:
            # Clock out the user
            try:
                last_clock_entry = ClockEntry.objects.filter(user=user, clock_out__isnull=True).latest('clock_in')
                last_clock_entry.clock_out =  timezone.localtime(timezone.now())
                
                # Calculate wages (convert hours_worked to Decimal)
                hourly_wage = user.hourly_wage
                rate = int(hourly_wage / 60)
                clock_in_time = timezone.make_naive( last_clock_entry.clock_in)
                clock_out_time =  timezone.make_naive( last_clock_entry.clock_out)
                minutes_worked = ((clock_out_time - clock_in_time).total_seconds()) / 60
                hours_worked_decimal = round(minutes_worked)  # Convert to Decimal
                print(f"Hours worked: {hours_worked_decimal}")
                last_clock_entry.wage = round(rate * hours_worked_decimal)  # Perform multiplication
                last_clock_entry.minuts_worked = hours_worked_decimal
                last_clock_entry.save()
                
                response_data['message'] = 'Clock out successful'
                response_data['user'] = user.username
                response_data['clock_in_time'] = clock_in_time
                response_data['clock_out_time'] = clock_out_time
                response_data['late'] = last_clock_entry.late_minutes
                response_data['wage'] = last_clock_entry.wage
                response_data['minuts_worked'] = hours_worked_decimal
                return Response(response_data, status=http_status.HTTP_200_OK)
            except ClockEntry.DoesNotExist:
                return Response({'message': 'Clock in before clocking out'}, status=http_status.HTTP_400_BAD_REQUEST)
            
class UserListCreateAPIView(APIView):
    def get(self, request):
        # Retrieve a list of users
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Check if a user with the same PIN already exists
        pin = request.data.get('pin')
        if User.objects.filter(pin=pin).exists():
            return Response({'message': 'User with this PIN already exists'}, status=http_status.HTTP_400_BAD_REQUEST)
        
        # Create a new user
        print(request.data)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            week_schedule_data = request.data.get('week_schedules', [])
            print(week_schedule_data)
            # Iterate through week_schedule_data and create WeekSchedule objects
            for schedule_data in week_schedule_data:
                schedule_data['user'] = user.id
                week_schedule_serializer = WeekScheduleSerializer(data=schedule_data)
                if week_schedule_serializer.is_valid():
                    week_schedule_serializer.save()
                else:
                    return Response(week_schedule_serializer.errors, status=http_status.HTTP_400_BAD_REQUEST)
            
            return Response(serializer.data, status=http_status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=http_status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response(status=http_status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=http_status.HTTP_404_NOT_FOUND)
    
class UserDetailAPIView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=http_status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=http_status.HTTP_404_NOT_FOUND)
        


class UserClockDataAPIView(APIView):
    def get(self, request, date):
        # Convert the date string to a date object (e.g., '2023-09-15')
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format'}, status=http_status.HTTP_400_BAD_REQUEST)

        # Query the database to get clock-in and clock-out data for all users on the specific date
        user_clock_data = []
        users = User.objects.all()  # Replace 'User' with your actual user model

        for user in users:
            clock_entries = ClockEntry.objects.filter(
                user=user,
                clock_in__date=date_obj
            )

            if clock_entries.exists():
                data = clock_entries.aggregate(
                    total_wage=Sum('wage'),  # Replace 'wage_field' with the actual field name for wage
                    total_minutes_worked=Sum('minuts_worked'),  # Replace 'minutes_worked_field'
                    first_late=Min('late_minutes'),  # Get the earliest late time
                    first_clock_in=Min('clock_in'),  # Get the earliest clock-in time
                    last_clock_out=Max('clock_out')  # Get the latest clock-out time
                )

                # Calculate wage, convert minutes to hours and minutes
                total_wage = data['total_wage'] or Decimal('0.00')  # Replace with your wage calculation logic
                total_minutes_worked = data['total_minutes_worked'] or 0
                total_hours_worked = total_minutes_worked // 60
                remaining_minutes = total_minutes_worked % 60

                # Append user-specific data to the list
                user_clock_data.append({
                    "user_id": user.id,
                    'username': user.username,
                    'wage': total_wage,
                    'minutes_worked': f'{total_hours_worked} hours {remaining_minutes} minutes',
                    'late': data['first_late'] or 0,  # Use the earliest late time or 0 if none
                    'first_clock_in': data['first_clock_in'],
                    'last_clock_out': data['last_clock_out'],
                })

        # Create a serialized response for the list of users
        serializer = UserClockDataSerializer(user_clock_data, many=True)

        return Response(serializer.data)
