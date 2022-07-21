from django.urls import path, include
from . import views


urlpatterns = [
    path('<page>', views.page, name='page'),
    path('', views.home, name='home'),
]
