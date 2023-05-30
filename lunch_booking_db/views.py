from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from .models import BookingInfo, ProfileInfoLunch
import datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from home.models import ProfileInfo


@login_required
def lunch_booking_db(request):
    tomorrow = add_days(1)
    try:
        booking = BookingInfo.objects.filter(user=request.user).get(date=tomorrow)
        booking.email = request.user.email
        booking.office_id = request.user.profileinfo.office_id_no
        booking.name = f"{request.user.first_name} {request.user.last_name}"
        booking.save(
            update_fields=['email', 'office_id', 'name']
        )
    except Exception as e:
        try:
            booking = BookingInfo()
            booking.user = request.user
            booking.date = tomorrow
            booking.email = request.user.email
            booking.office_id = request.user.profileinfo.office_id_no
            booking.name = f"{request.user.first_name} {request.user.last_name}"
            booking.booked = 'no'
            booking.save()
        except Exception as e:
            return render(request, 'lunch_booking_db/index.html', {})

    try:
        user_id = ProfileInfo.objects.get(request.user).office_id_no
    except Exception as e:
        user_id = 'n/a'

    context = {
        'booking': booking,
        'user_id': user_id
    }
    return render(request, 'lunch_booking_db/index.html', context)


# def test_ntf(request):
#     context = {
#
#     }
#     return render(request, 'lunch_booking/test.html', context)

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required
def ajax_register_office_id(request):
    if request.method == "POST" and is_ajax(request=request):
        try:
            user_profile = ProfileInfo.objects.get(user=request.user)
            user_profile.office_id_no = request.POST.get('id', None)
            user_profile.save(
                update_fields=['office_id_no']
            )
        except Exception as e:
            user_profile = ProfileInfo()
            user_profile.user = request.user
            user_profile.office_id_no = request.POST.get('id', None)
            user_profile.save()

        try:
            instance = ProfileInfo.objects.get(user=request.user)
            instance.profile_type = 'general'
            instance.save(
                update_fields=['profile_type']
            )
        except Exception as e:
            instance = ProfileInfoLunch(user=request.user)
            instance.profile_type = 'general'
            instance.save()

        return JsonResponse({'success': True}, status=200)
    return JsonResponse({'success': False}, status=400)


@login_required
def ajax_save_notification_token(request):
    if request.method == "POST" and is_ajax(request=request):
        try:
            instance = ProfileInfo.objects.get(user=request.user)
            instance.notification_token = request.POST.get('notification_token', None)
            instance.save(
                update_fields=['notification_token']
            )
            return JsonResponse({'success': True}, status=200)
        except Exception as e:
            return JsonResponse({'success': False}, status=200)
    return JsonResponse({'success': False}, status=400)


@login_required
def ajax_book_lunch(request):
    if request.method == "POST" and is_ajax(request=request):
        days = int(request.POST.get('day', 1))
        try:
            instance = BookingInfo.objects.filter(user=request.user).get(date=add_days(days))
            instance.booked = request.POST.get('booking', None)
            instance.email = request.user.email
            instance.office_id = request.user.profileinfo.office_id_no
            instance.name = f"{request.user.first_name} {request.user.last_name}"
            instance.save(
                update_fields=['booked', 'email', 'office_id', 'name']
            )
        except Exception as e:
            instance = BookingInfo()
            instance.user = request.user
            instance.date = add_days(days)
            instance.email = request.user.email
            instance.office_id = request.user.profileinfo.office_id_no
            instance.name = f"{request.user.first_name} {request.user.last_name}"
            instance.booked = request.POST.get('booking', None)
            instance.save()
        return JsonResponse({'success': True}, status=200)
    return JsonResponse({'success': False}, status=400)


@login_required
def ajax_get_booking_count(request):
    if request.method == "GET" and is_ajax(request=request):
        bookings = BookingInfo.objects.filter(date=add_days(1)).filter(booked='yes')
        count = len(bookings)
        return JsonResponse({'success': True, 'count': count}, status=200)
    return JsonResponse({'success': False}, status=400)


@login_required
def ajax_get_booking_of_date(request):
    if request.method == "GET" and is_ajax(request=request):
        final_list = []
        for i in range(-2, 5, 1):
            try:
                booking_status = BookingInfo.objects.filter(user=request.user).get(date=add_days(i)).booked
                final_list.append(booking_status)

            except Exception as e:
                final_list.append('n/a')

        return JsonResponse({'success': True, 'status': final_list}, status=200)
    return JsonResponse({'success': False}, status=400)


@login_required
def ajax_check_office_id(request):
    if request.method == "GET" and is_ajax(request=request):
        try:
            office_id = ProfileInfo.objects.get(user=request.user).office_id_no
        except Exception as e:
            office_id = 'n/a'
        try:
            status = BookingInfo.objects.filter(user=request.user).get(date=add_days(1)).booked
        except Exception as e:
            return JsonResponse({'success': True, 'office_id': 'n/a'}, status=200)

        if status == 'yes':
            status = 'Y'
        else:
            status = 'N'

        try:
            user_type = ProfileInfoLunch.objects.get(user=request.user).profile_type
        except Exception as e:
            instance = ProfileInfoLunch(user=request.user)
            instance.profile_type = 'general'
            instance.save()
            user_type = 'general'

        return JsonResponse({'success': True, 'office_id': office_id, 'status': status, 'user_type': user_type}, status=200)
    return JsonResponse({'success': False}, status=400)


@login_required
def serve_booking_list(request):
    if request.method == "GET" and is_ajax(request=request):
        date = request.GET.get('date', None)

        bookings = list(BookingInfo.objects.filter(
            date=date
        ).filter(booked='yes').order_by('office_id').values())

        return JsonResponse(data={"lunch_data": bookings}, status=200, safe=False)
    return JsonResponse({}, status=400)


def service_worker(request):
    sw_path = settings.BASE_DIR / "lunch_booking/static/lunch_booking/js" / "firebase-messaging-sw.js"
    response = HttpResponse(open(sw_path).read(), content_type='application/javascript')
    return response


def add_days(days):
    new_date = datetime.date.today() + datetime.timedelta(days=days)
    return new_date
