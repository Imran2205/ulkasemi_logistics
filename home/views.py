from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
from .models import ProfileInfo
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount


def home(request):
    context = {

    }
    return render(request, 'home/home.html', context)


def login(request):
    context = {

    }
    return render(request, 'home/login.html', context)


@login_required()
def populate_values(request):
    try:
        p_i = ProfileInfo.objects.get(user=request.user)
        p_i.profile_picture_url = SocialAccount.objects.get(user=request.user).extra_data['picture']
        p_i.save(update_fields=['profile_picture_url'])
        return JsonResponse({"status": "success"}, status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"status": "failed"}, status=400)
