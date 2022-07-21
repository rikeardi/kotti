from django.shortcuts import render
from .models import *


# Create your views here.
def home(request):
    context = {
        'headers': DocsHeader.objects.all(),
        'pages': DocsPage.objects.all(),
        'chapters': DocsChapter.objects.all(),
        'page': None,
    }
    return render(request, 'docs/front.html', context)


def page(request, page_name):
    page = DocsPage.objects.get(title=page_name)
    context = {
        'page': page,
        'chapters': DocsChapter.objects.filter(page_id=page.id),
    }
    return render(request, 'docs/front.html', context)
