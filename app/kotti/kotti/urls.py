"""tilkku URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from main import api

router = routers.DefaultRouter()
router.register(r'rooms', api.RoomViewSet)
router.register(r'tables', api.TableViewSet)
router.register(r'table_reservations', api.TableReservationViewSet)
router.register(r'open_times', api.OpenTimeViewSet)
router.register(r'users', api.KottiUserViewSet)
router.register(r'open_days', api.OpenDayViewSet)
router.register(r'room_times', api.OpenDayViewSet)


urlpatterns = [
    path('', include('main.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
