import pyrebase
import streamlit as st
from datetime import datetime


def app():


     firebaseConfig = {'apiKey': "AIzaSyBh4Kj5gBFW5ahZWnlis75iarYqxTsvCuk",
        'authDomain': "test-streamlit-acd50.firebaseapp.com",
        'projectId': "test-streamlit-acd50",
        'storageBucket': "test-streamlit-acd50.appspot.com",
        'messagingSenderId': "406686388491",
        'appId': "1:406686388491:web:3fa0b8fd427ec8f9b2920e",
        'measurementId': "G-Q01C3WELQX",
        'databaseURL' : "https://test-streamlit-acd50-default-rtdb.europe-west1.firebasedatabase.app/"
        }


     firebase = pyrebase.initialize_app(firebaseConfig)
     auth = firebase.auth()


     db = firebase.database()
     storage = firebase.storage()
     st.sidebar.title("Bienvenue sur la communaute des visualisations boursieres")

     choice = st.sidebar.selectbox('login/Signup', ['Login', 'Sign up'])


     email = st.sidebar.text_input('Please enter your email address')
     password = st.sidebar.text_input('Please enter your password',type = 'password')

     if choice == 'Sign up':
        handle = st.sidebar.text_input(
            'Please input your app handle name', value='Default')
        submit = st.sidebar.button('Create my account')

        if submit:
            user = auth.create_user_with_email_and_password(email, password)
            st.success('Your account is created suceesfully!')
            st.balloons()

            user = auth.sign_in_with_email_and_password(email, password)
            db.child(user['localId']).child("Handle").set(handle)
            db.child(user['localId']).child("ID").set(user['localId'])
            st.title('Welcome' + handle)
            st.info('Login via login drop down selection')
