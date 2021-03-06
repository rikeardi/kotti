from django.contrib.auth.decorators import login_required
from django.urls import path, include
import django.contrib.auth.views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from . import views, forms

app_name = 'main'
urlpatterns = [
    path('', views.home, name='home'),
    path('status/', views.status, name='status'),
    path('accounts/login/', django.contrib.auth.views.LoginView.as_view(authentication_form=forms.LoginForm), name='login'),
    path('accounts/create/', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
]
