from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse


def home(request):
    context = {

    }
    return render(request, 'home/home.html', context)
