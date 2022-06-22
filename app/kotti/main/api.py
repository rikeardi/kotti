from rest_framework import serializers, viewsets
from .models import *


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name', 'description', 'accept_limit', 'open_times')


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


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


class OpenTimeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OpenTime
        fields = ('id', 'start_time', 'end_time')


class OpenTimeViewSet(viewsets.ModelViewSet):
    queryset = OpenTime.objects.all()
    serializer_class = OpenTimeSerializer


class KottiUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KottiUser
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'department', 'team')


class KottiUserViewSet(viewsets.ModelViewSet):
    queryset = KottiUser.objects.all()
    serializer_class = KottiUserSerializer
