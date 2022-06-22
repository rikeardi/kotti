from django.contrib.auth.decorators import login_required
from django.urls import path, include
import django.contrib.auth.views
from django.views.generic import TemplateView

from . import views, forms

app_name = 'main'
urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', django.contrib.auth.views.LoginView.as_view(authentication_form=forms.LoginForm), name='login'),
    path('accounts/create/', django.contrib.auth.views.FormView.as_view(form_class=forms.RegisterForm, success_url='/', template_name='registration/register.html'), name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
]