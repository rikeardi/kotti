import json

from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home(request):
    context = {
    }
    return render(request, 'front.html', context)


def register(request):
    context = {
    }
    return render(request, 'registration/register.html', context)