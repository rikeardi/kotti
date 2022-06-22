from django.contrib import admin

# Register your models here.
from django.contrib import admin
from main.models import *

admin.site.register(KottiUser)
admin.site.register(OpenTime)
admin.site.register(Room)
admin.site.register(Table)
admin.site.register(TableReservation)