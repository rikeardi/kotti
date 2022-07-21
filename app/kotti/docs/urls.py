from django.urls import path, include
from . import views


urlpatterns = [
    path('<page_name>/', views.page, name='page'),
    path('', views.home, name='home'),
]
