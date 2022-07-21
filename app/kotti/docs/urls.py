from django.urls import path, include
from . import views


urlpatterns = [
    path('new-header/', views.new_header, name='new_header'),
    path('new-page/', views.new_page, name='new_page'),
    path('pages/<id>/', views.page_edit, name='page'),
    path('<page_name>/', views.page, name='page'),
    path('', views.home, name='home'),
]
