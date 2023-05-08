from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.lunch_booking, name='lunch_booking'),
]