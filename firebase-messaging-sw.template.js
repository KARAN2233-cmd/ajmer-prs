/* Firebase Cloud Messaging service worker.
   Must sit in the SAME folder as index.html on GitHub Pages.
   The values are filled in by GitHub when the page is published. */
importScripts('https://www.gstatic.com/firebasejs/10.12.2/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.12.2/firebase-messaging-compat.js');

firebase.initializeApp({
  apiKey: 'FIREBASE_API_KEY',
  authDomain: 'FIREBASE_AUTH_DOMAIN',
  projectId: 'FIREBASE_PROJECT_ID',
  storageBucket: 'FIREBASE_STORAGE_BUCKET',
  messagingSenderId: 'FIREBASE_MESSAGING_SENDER_ID',
  appId: 'FIREBASE_APP_ID'
});

// Messages that carry a "notification" block are shown by Firebase itself while
// the page is closed, and tapping them opens the requisition app (fcm_options.link).
firebase.messaging();
