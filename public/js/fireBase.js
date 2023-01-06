// Import the functions you need from the SDKs you need
var { initializeApp } = require("firebase/app");
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDv9IlXP2pR7eJwX9jie1L9BtgkLnrQFac",
  authDomain: "re-remote-control.firebaseapp.com",
  projectId: "re-remote-control",
  storageBucket: "re-remote-control.appspot.com",
  messagingSenderId: "225546835794",
  appId: "1:225546835794:web:e1d1c6a25359a00792cc8b"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);