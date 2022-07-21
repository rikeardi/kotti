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
from sphinx_view import DocumentationView
from main import api

router = routers.DefaultRouter()
router.register(r'room', api.RoomViewSet)
router.register(r'rooms', api.RoomList, basename='Room')
router.register(r'room_times', api.RoomTimeViewSet)
router.register(r'open_days', api.OpenDayViewSet)
router.register(r'open_times', api.OpenTimeViewSet)
router.register(r'booking', api.BookingViewSet)
router.register(r'users', api.KottiUserViewSet)


urlpatterns = [
    path('', include('main.urls')),
    path('docs<path:path>', DocumentationView.as_view(json_build_dir='docs/_build/json',
                                                      base_template_name='templates/docs/base.html'), name='docs'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]

