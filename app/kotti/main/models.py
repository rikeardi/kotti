"""
Django models for room management.

Rooms and tables are used to manage the seating capacity of a room.
"""
from django.db import models
from django.contrib.auth.models import User, AbstractUser


class KottiUser(AbstractUser):
    """
    User model for the room management app.
    """
    password = models.CharField(max_length=128, verbose_name="password")
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=100, choices=[('LT', 'Leiritoimikunta'), ('EL', 'Elämys'),
                                                           ('OS', 'Osallistujat'), ('PA', 'Palvelut'),
                                                           ('KA', 'Kasvatus'), ('RE', 'Resurssit')])
    team = models.CharField(max_length=200)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class OpenTime(models.Model):
    """
    Model for the opening times of the room.
    """
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return str(self.start_time) + " - " + str(self.end_time)


class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    admins = models.ManyToManyField('KottiUser', related_name='admin_of_rooms', blank=True)
    accept_limit = models.IntegerField(default=100)
    open_times = models.ManyToManyField(OpenTime, blank=True)

    def __str__(self):
        return self.name


class Table(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name


class TableReservation(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    user = models.ForeignKey('KottiUser', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f'{self.user.team} - {self.table.name}'
