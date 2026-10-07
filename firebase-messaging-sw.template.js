/* Firebase Cloud Messaging service worker.
   Must sit in the SAME folder as index.html on GitHub Pages.
   The values are filled in by GitHub when the page is published. */
importScripts('https://www.gstatic.com/firebasejs/10.12.2/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.12.2/firebase-messaging-compat.js');

firebase.initializeApp({
  apiKey: '__FIREBASE_API_KEY__',
  authDomain: '__FIREBASE_AUTH_DOMAIN__',
  projectId: '__FIREBASE_PROJECT_ID__',
  storageBucket: '__FIREBASE_STORAGE_BUCKET__',
  messagingSenderId: '__FIREBASE_MESSAGING_SENDER_ID__',
  appId: '__FIREBASE_APP_ID__'
});

// Messages that carry a "notification" block are shown by Firebase itself while
// the page is closed, and tapping them opens the requisition app (fcm_options.link).
firebase.messaging();
