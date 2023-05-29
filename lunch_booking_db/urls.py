from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.lunch_booking_db, name='lunch_booking_db'),
    path('ajax-register-office-id/', views.ajax_register_office_id, name='ajax_register_office_id'),
    path('ajax-check-office-id/', views.ajax_check_office_id, name='ajax_check_office_id')
]
