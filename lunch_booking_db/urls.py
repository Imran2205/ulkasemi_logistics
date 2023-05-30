from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.lunch_booking_db, name='lunch_booking_db'),
    path('ajax-register-office-id/', views.ajax_register_office_id, name='ajax_register_office_id'),
    path('ajax-check-office-id/', views.ajax_check_office_id, name='ajax_check_office_id'),
    path('ajax-save-notification-token/', views.ajax_save_notification_token, name='ajax_save_notification_token'),
    path('ajax-book-lunch/', views.ajax_book_lunch, name='ajax_book_lunch'),
    path('ajax-get-booking-count/', views.ajax_get_booking_count, name='ajax_get_booking_count'),
    path('serve-booking-list/', views.serve_booking_list, name='serve_booking_list'),
    path('ajax-get-booking-of-date/', views.ajax_get_booking_of_date, name='ajax_get_booking_of_date')
]
