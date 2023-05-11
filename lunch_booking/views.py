from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse


def lunch_booking(request):
    context = {

    }
    return render(request, 'lunch_booking/index.html', context)


# def test_ntf(request):
#     context = {
#
#     }
#     return render(request, 'lunch_booking/test.html', context)


def service_worker(request):
    sw_path = settings.BASE_DIR / "lunch_booking/static/lunch_booking/js" / "firebase-messaging-sw.js"
    response = HttpResponse(open(sw_path).read(), content_type='application/javascript')
    return response
