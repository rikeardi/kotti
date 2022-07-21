from django.shortcuts import render
from .models import *


# Create your views here.
def home(request):
    context = {
        'headers': DocsHeader.objects.all(),
    }
    return render(request, 'docs/front.html', context)
