import json
from datetime import datetime

from django.db.models import Q
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


class BookingSerializer(serializers.HyperlinkedModelSerializer):
    user = KottiUserSerializer(read_only=True)
    date = OpenDaySerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ('id', 'user', 'date', 'start_time', 'end_time', 'persons', 'approved', 'information')


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        instance = Booking.objects.create(user=request.user, date=OpenDay.objects.get(pk=request.data.get('date')),
                                          start_time=request.data.get('start_time'),
                                          end_time=request.data.get('end_time'), persons=request.data.get('persons'),
                                          information=request.data.get('information'))
        room = Room.objects.get(pk=request.data.get('room'))
        room.bookings.add(instance)
        room.save()
        return Response(BookingSerializer(instance).data)

    def get_queryset(self):
        queryset = Booking.objects.all()

        user = self.request.query_params.get('user')
        if user:
            queryset = queryset.filter(user__id=user)

        return queryset

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        approved = request.data.get('approved')
        if approved:
            instance.approved = approved

        information = request.data.get('information')
        if information:
            instance.information = information

        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class RoomSerializer(serializers.ModelSerializer):
    open_times = RoomTimeSerializer(many=True)
    bookings = BookingSerializer(many=True)
    admins = KottiUserSerializer(many=True)
    availability = serializers.ReadOnlyField(source='get_availability')

    class Meta:
        model = Room
        fields = ('id', 'name', 'description', 'capacity', 'equipment', 'admins', 'open_times', 'bookings', 'availability')


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def create(self, request, *args, **kwargs):
        instance = Room.objects.create(name=request.data.get('name'), description=request.data.get('description'),
                                       capacity=request.data.get('capacity'), equipment=request.data.get('equipment'))

        admins = json.loads(request.data.get('admins'))
        if admins:
            for admin in admins:
                instance.admins.add(KottiUser.objects.get(pk=admin))
        else:
            instance.admins.add(request.user)

        instance.save()
        return Response(RoomSerializer(instance).data)

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

        admins = request.data.get('admins')
        if admins:
            instance.admins.clear()
            for admin in json.loads(admins):
                instance.admins.add(KottiUser.objects.get(pk=admin))

        name = request.data.get('name')
        if name:
            instance.name = name

        description = request.data.get('description')
        if description:
            instance.description = description

        equipment = request.data.get('equipment')
        if equipment:
            instance.equipment = equipment

        capacity = request.data.get('capacity')
        if capacity:
            instance.capacity = int(capacity)

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

        booking_user = self.request.query_params.get('booking_user')
        if booking_user:
            queryset = queryset.filter(bookings__user__id=booking_user).distinct()

        admin = self.request.query_params.get('admin')
        if admin:
            queryset = queryset.filter(admins__id=admin)

        bookings = self.request.query_params.get('bookings')
        if bookings:
            queryset = queryset.filter(bookings__isnull=False)

        old = self.request.query_params.get('old')
        current = self.request.query_params.get('current')
        future = self.request.query_params.get('future')
        if old or current or future:
            old_q = Q()
            current_q = Q()
            future_q = Q()

            if old:
                old_q = Q(bookings__date__date__lte=datetime.now().date())
            if current:
                current_q = Q(bookings__date__date=datetime.now().date())
            if future:
                future_q = Q(bookings__date__date__gte=datetime.now().date())

            queryset = queryset.filter(old_q | current_q | future_q).distinct()

        waiting = self.request.query_params.get('waiting')
        approved = self.request.query_params.get('approved')
        denied = self.request.query_params.get('denied')
        cancelled = self.request.query_params.get('cancelled')
        if waiting or approved or denied or cancelled:
            wait_q = Q()
            approved_q = Q()
            denied_q = Q()
            cancelled_q = Q()

            if waiting:
                wait_q = Q(bookings__approved=0)
            if approved:
                approved_q = Q(bookings__approved=1)
            if denied:
                denied_q = Q(bookings__approved=2)
            if cancelled:
                cancelled_q = Q(bookings__approved=3)

            queryset = queryset.filter(wait_q | approved_q | denied_q | cancelled_q)

        return queryset.distinct()


class KottiUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KottiUser
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'department', 'team')


class KottiUserViewSet(viewsets.ModelViewSet):
    queryset = KottiUser.objects.all()
    serializer_class = KottiUserSerializer
