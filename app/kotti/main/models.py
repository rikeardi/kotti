"""
Django models for room management.

Rooms and tables are used to manage the seating capacity of a room.
"""

from datetime import datetime, date, timedelta

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class KottiUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, first_name=None, last_name=None, phone=None, department=None, team=None):

        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            department=department,
            team=team,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email=None, first_name=None, last_name=None, phone=None, department=None, team=None):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            department=department,
            team=team,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class KottiUser(AbstractBaseUser):
    """
    User model for the room management app.
    """
    password = models.CharField(max_length=128, verbose_name="password")
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=100, choices=[('Leiritoimikunta', 'Leiritoimikunta'), ('Elämys', 'Elämys'),
                                                           ('Osallistujat', 'Osallistujat'), ('Palvelut', 'Palvelut'),
                                                           ('Kasvatus', 'Kasvatus'), ('Resurssit', 'Resurssit')],
                                  blank=True, null=True)
    team = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_room_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = KottiUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class OpenDay(models.Model):
    """
    Model for the open days of the room management app.
    """
    name = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return f'{self.name} - {self.date.strftime("%-d.%-m.")}'


class OpenTime(models.Model):
    """
    Model for the opening times of the room.
    """
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return str(self.start_time) + " - " + str(self.end_time)


class RoomTime(models.Model):
    """
    Model for the opening times of the room.
    """
    day = models.ForeignKey('OpenDay', on_delete=models.CASCADE)
    times = models.ManyToManyField(OpenTime, blank=True)

    def __str__(self):
        return self.day.name


class Booking(models.Model):
    """
    Model for the bookings of the room management app.
    """
    user = models.ForeignKey('KottiUser', on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.ForeignKey('OpenDay', on_delete=models.CASCADE)
    persons = models.IntegerField(default=2)
    approved = models.IntegerField(default=0, choices=[(0, 'Odottaa hyväksyntää'), (1, 'Hyväksytty'), (2, 'Hylätty')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.team} - {self.date.name} - {self.start_time} - {self.end_time}'


class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    equipment = models.TextField(blank=True)
    admins = models.ManyToManyField('KottiUser', related_name='admin_of_rooms', blank=True)
    capacity = models.IntegerField(default=0)
    accept_limit = models.IntegerField(default=100)
    open_times = models.ManyToManyField(RoomTime, blank=True)
    bookings = models.ManyToManyField(Booking, blank=True)

    def __str__(self):
        return f'{self.name} ({self.capacity})'

    @property
    def get_availability(self):
        """
        Returns the availability of the room.
        """
        availability = []

        for open_time in self.open_times.all():
            day_availability = {'day': open_time.day.id, 'times': []}
            for opening_time in open_time.times.all():
                avail_time = opening_time.start_time
                while avail_time < opening_time.end_time:
                    time_availability = {'time': avail_time.strftime("%H:%M"), 'available': self.capacity}
                    day_availability['times'].append(time_availability)
                    avail_time = (datetime.combine(date.today(), avail_time) + timedelta(minutes=15)).time()

            availability.append(day_availability)

        for booking in self.bookings.all():
            if booking.approved == 2:
                break
            for day in availability:
                print(day);
                if day['day'] == booking.date.id:
                    for time in day['times']:
                        print(time);
                        if booking.start_time.strftime("%H:%M") <= time['time'] < booking.end_time.strftime("%H:%M"):
                            time['available'] -= booking.persons

        return availability

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save(force_insert, force_update, using, update_fields)
        for admin in self.admins.all():
            admin.is_room_admin = True
            admin.save()


