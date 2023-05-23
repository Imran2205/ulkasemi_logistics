from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('upp/', views.populate_values, name='update_profile_picture'),
]
