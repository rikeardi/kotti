from django.urls import path, include
from . import views


urlpatterns = [
    path('new-header/', views.new_header, name='new_header'),
    path('new-page/', views.new_page, name='new_page'),
    path('pages/<id>/delete/', views.page_delete, name='page_delete'),
    path('pages/<id>/', views.page_edit, name='page_edit'),
    path('<page_name>/', views.page, name='page'),
    path('', views.home, name='home'),
]
