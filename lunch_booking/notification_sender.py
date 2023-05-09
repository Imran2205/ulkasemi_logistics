import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings

cred_path = settings.BASE_DIR / "lunch_booking/static/lunch_booking/json" / "firebase.json"
firebase_cred = credentials.Certificate(cred_path)

firebase_app = firebase_admin.initialize_app(firebase_cred)

message = messaging.Message(
    data={
        'title': 'Have you booked your lunch for tomorrow?',
        'text': 'Please book your lunch by 8 p.m. Click on the notification to visit lunch booking URL. If you have already booked your lunch then please ignore this notification.',
        'url': 'https://www.ulka.autos/lunch-booking'
    },
    topic='all'
)

response = messaging.send(message)
print('Successfully sent message:', response)
