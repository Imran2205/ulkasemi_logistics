import firebase_admin
from firebase_admin import credentials, messaging

firebase_cred = credentials.Certificate(r"C:\Users\admin\Desktop\desktop\web\lunch_booking\json\firebase.json")
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
