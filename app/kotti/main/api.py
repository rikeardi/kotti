from rest_framework import serializers, viewsets, generics
from rest_framework.response import Response
from .models import *


class KottiUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = KottiUser
        fields = ('id', 'first_name', 'last_name', 'department', 'team', 'phone', 'email')


class KottiUserViewSet(viewsets.ModelViewSet):
    queryset = KottiUser.objects.all()
    serializer_class = KottiUserSerializer


class OpenDaySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OpenDay
        fields = ('id', 'name', 'date')


class OpenDayViewSet(viewsets.ModelViewSet):
    queryset = OpenDay.objects.all()
    serializer_class = OpenDaySerializer


class OpenTimeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OpenTime
        fields = ('id', 'start_time', 'end_time')


class OpenTimeViewSet(viewsets.ModelViewSet):
    queryset = OpenTime.objects.all()
    serializer_class = OpenTimeSerializer


class RoomTimeSerializer(serializers.HyperlinkedModelSerializer):
    day = OpenDaySerializer(read_only=True)
    times = OpenTimeSerializer(many=True, read_only=True)

    class Meta:
        model = RoomTime
        fields = ('id', 'day', 'times')


class RoomTimeViewSet(viewsets.ModelViewSet):
    queryset = RoomTime.objects.all()
    serializer_class = RoomTimeSerializer


class RoomSerializer(serializers.ModelSerializer):
    open_times = RoomTimeSerializer(many=True)
    admins = KottiUserSerializer(many=True)

    class Meta:
        model = Room
        fields = ('id', 'name', 'description', 'capacity', 'equipment', 'admins', 'open_times')


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        day_id = request.data.get('day')

        if day_id:
            day = OpenDay.objects.get(pk=day_id)
            time = OpenTime.objects.create(start_time=start_time, end_time=end_time)

            if instance.open_times.filter(day=day).exists():
                existing_day = instance.open_times.get(day=day)
                existing_day.times.add(time)
                existing_day.save()
            else:
                new_day = RoomTime.objects.create(day=day, room=instance)
                new_day.times.add(time)
                instance.open_times.add(new_day)

        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class RoomList(viewsets.ModelViewSet):
    serializer_class = RoomSerializer

    def get_queryset(self):
        queryset = Room.objects.all()

        day = self.request.query_params.get('day')
        if day:
            queryset = queryset.filter(open_times__day__id=day)

        seats = self.request.query_params.get('seats')
        if seats:
            queryset = queryset.filter(capacity__gte=seats)

        return queryset


class BookingSerializer(serializers.HyperlinkedModelSerializer):
    user = KottiUserSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ('id', 'user', 'start_time', 'end_time')


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class KottiUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KottiUser
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'department', 'team')


class KottiUserViewSet(viewsets.ModelViewSet):
    queryset = KottiUser.objects.all()
    serializer_class = KottiUserSerializer
