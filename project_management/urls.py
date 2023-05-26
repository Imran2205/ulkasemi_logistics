from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.project_management, name='project_management'),
    path('ajax/create_project', views.ajax_create_project, name='create_project'),
    path('ajax/get_project/<int:pk>', views.ajax_get_proj, name='get_proj'),
    path('ajax/post_update/<int:pk>', views.ajax_post_update, name='post_update'),
]
