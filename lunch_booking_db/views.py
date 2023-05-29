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
    except Exception as e:
        booking = BookingInfo()
        booking.user = request.user
        booking.date = tomorrow
        booking.booked = 'no'
        booking.save()

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
def ajax_check_office_id(request):
    if request.method == "GET" and is_ajax(request=request):
        try:
            office_id = ProfileInfo.objects.get(user=request.user).office_id_no
        except Exception as e:
            office_id = 'n/a'
        status = BookingInfo.objects.filter(user=request.user).get(date=add_days(1)).booked
        if status == 'yes':
            status = 'Y'
        else:
            status = 'N'

        try:
            user_type = ProfileInfoLunch.objects.get(user=request.user).profile_type
        except Exception as e:
            user_type = 'general'

        return JsonResponse({'success': True, 'office_id': office_id, 'status': status, 'user_type': user_type}, status=200)
    return JsonResponse({'success': False}, status=400)


def service_worker(request):
    sw_path = settings.BASE_DIR / "lunch_booking/static/lunch_booking/js" / "firebase-messaging-sw.js"
    response = HttpResponse(open(sw_path).read(), content_type='application/javascript')
    return response


def add_days(days):
    new_date = datetime.date.today() + datetime.timedelta(days=days)
    return new_date
