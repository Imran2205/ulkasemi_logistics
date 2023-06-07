from django.urls import path, include
from . import views
import allauth


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('upp/', views.populate_values, name='update_profile_picture'),
]
