from rest_framework import serializers, viewsets, generics
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
    day = OpenDaySerializer()
    times = OpenTimeSerializer(many=True)

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


class TableSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Table
        fields = ('id', 'room', 'name', 'capacity')


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class TableReservationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TableReservation
        fields = ('id', 'table', 'user', 'start_time', 'end_time')


class TableReservationViewSet(viewsets.ModelViewSet):
    queryset = TableReservation.objects.all()
    serializer_class = TableReservationSerializer


class KottiUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KottiUser
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'department', 'team')


class KottiUserViewSet(viewsets.ModelViewSet):
    queryset = KottiUser.objects.all()
    serializer_class = KottiUserSerializer
