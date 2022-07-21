from django.shortcuts import render, redirect
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
        'headers': DocsHeader.objects.all(),
        'pages': DocsPage.objects.all(),
        'chapters': DocsChapter.objects.all(),
        'page': page,
        'page_chapters': DocsChapter.objects.filter(page_id=page.id),
    }
    return render(request, 'docs/front.html', context)


def page_edit(request, page_id):
    page = DocsPage.objects.get(id=page_id)

    if request.method == 'PATCH':
        page.title = request.POST['title'].lower()
        page.header_id = request.POST['header_id']
        page.save()
        return redirect('/docs/' + page.title + '/')

    if request.method == 'DELETE':
        page.delete()
        return redirect('/docs/')

    return redirect('/docs/' + page.title + '/')


def new_header(request):
    if request.method == 'POST':
        header = DocsHeader.objects.create(title=request.POST['title'].lower())
        header.save()
        return redirect('/docs/')


def new_page(request):
    if request.method == 'POST':
        print(request.POST)
        page = DocsPage.objects.create(title=request.POST['title'].lower(),
                                       header_id=request.POST['header_id'])
        page.save()
        return redirect('/docs/' + page.title + '/')
