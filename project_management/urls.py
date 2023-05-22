from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.project_management, name='project_management'),
    path('ajax/create_project', views.ajax_create_project, name='create_project'),
]
