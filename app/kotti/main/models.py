"""
Django models for room management.

Rooms and tables are used to manage the seating capacity of a room.
"""
import time

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
    department = models.CharField(max_length=100, choices=[('LT', 'Leiritoimikunta'), ('EL', 'Elämys'),
                                                           ('OS', 'Osallistujat'), ('PA', 'Palvelut'),
                                                           ('KA', 'Kasvatus'), ('RE', 'Resurssit')],
                                  default='LT', blank=True, null=True)
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
    selected_room = models.ForeignKey('Room', on_delete=models.CASCADE)

    def __str__(self):
        return self.day.name


class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    equipment = models.TextField(blank=True)
    admins = models.ManyToManyField('KottiUser', related_name='admin_of_rooms', blank=True)
    capacity = models.IntegerField(default=0)
    accept_limit = models.IntegerField(default=100)
    open_times = models.ManyToManyField(RoomTime, blank=True)

    def __str__(self):
        return f'{self.name} ({self.capacity})'

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save(force_insert, force_update, using, update_fields)
        for admin in self.admins.all():
            admin.is_room_admin = True
            admin.save()


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
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.team} - {self.table.name}'
