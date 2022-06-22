from django.contrib import admin

# Register your models here.
from django.contrib import admin
from main.models import *


class KottiUserAdmin(admin.StackedInline):
    model = KottiUser
    can_delete = False
    verbose_name_plural = 'KottiUsers'


class UserAdmin(admin.UserAdmin):
    inlines = (KottiUserAdmin,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(OpenTime)
admin.site.register(Room)
admin.site.register(Table)
admin.site.register(TableReservation)