from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.project_management, name='project_management'),
    path('ajax/create_project', views.ajax_create_project, name='create_project'),
    path('ajax/get_project/<int:pk>', views.ajax_get_proj, name='get_proj'),
    path('ajax/post_update/<int:pk>', views.ajax_post_update, name='post_update'),
    path('ajax/set_project_progress/', views.set_project_progress, name='set_project_progress'),
    path('ajax/set_project_status/', views.set_project_status, name='set_project_status'),
    path('ajax/set_project_progress/', views.set_project_progress, name='set_project_progress'),
    path('ajax/get_user_pop_up_info/', views.get_user_pop_up_info, name='get_user_pop_up_info'),
    path('create_teams/', views.create_teams, name='create_teams'),
]
