from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.project_management, name='project_management')
]
