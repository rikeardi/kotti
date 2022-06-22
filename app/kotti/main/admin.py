from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from main.models import *


class KottiUserAdmin(admin.StackedInline):
    model = KottiUser
    can_delete = False
    verbose_name_plural = 'KottiUsers'


class UserAdmin(UserAdmin):
    inlines = (KottiUserAdmin,)


#admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(OpenTime)
admin.site.register(Room)
admin.site.register(Table)
admin.site.register(TableReservation)