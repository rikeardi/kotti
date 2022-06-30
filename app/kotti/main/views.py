import datetime
import json

from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import *


@login_required
def home(request):
    context = {
        'open_days': OpenDay.objects.all().filter(date__gte=datetime.date.today()).order_by('date'),
        'rooms': Room.objects.all(),
        'users': KottiUser.objects.all(),
    }
    return render(request, 'front.html', context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/accounts/login/')
        else:
            return render(request, 'registration/register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'registration/register.html', {'form': form})
