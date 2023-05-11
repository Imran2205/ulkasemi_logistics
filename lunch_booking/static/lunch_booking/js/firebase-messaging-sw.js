importScripts('https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js');
//Remeber this part we have used above in our index.html
var firebaseConfig = {
  apiKey: "AIzaSyBrbp6qgMQTdulFTl3oupuQa1_4G6zvBsk",
  authDomain: "lunch-booking-380210.firebaseapp.com",
  projectId: "lunch-booking-380210",
  storageBucket: "lunch-booking-380210.appspot.com",
  messagingSenderId: "1058830329036",
  appId: "1:1058830329036:web:f562cbee96fb5a4a01ce69",
  measurementId: "G-X3RHXPY5BM"
};
firebase.initializeApp(firebaseConfig);
// firebase.analytics();
const messaging = firebase.messaging();
var url = "https://www.ulka.autos/lunch_booking/"
messaging.onBackgroundMessage(function(payload) {
  console.log('[firebase-messaging-sw.js] Received background message ', payload);
  // Customize notification here
  const notificationTitle = payload['data']['title'];
  // console.log("sssss");
  // console.log(payload['data']);
  url = payload['data']['url'];
  const notificationOptions = {
    body: payload['data']['text'],
    icon: 'https://github.com/Imran2205/lunch_booking/raw/master/images/food.png'
  };
  self.registration.showNotification(notificationTitle,
        notificationOptions);
  // var notification = new Notification(notificationTitle, notificationOptions);
  // notification.onclick = function() {
  //     window.location.href = payload['data']['url'];
  // };
});

self.addEventListener('notificationclick', event => {
   // window.location.href = "https://imran2205.github.io/lunch_booking/";
   clients.openWindow(url);
});