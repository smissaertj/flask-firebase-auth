import firebase_admin

import pyrebase
from datetime import datetime, timedelta
from firebase_admin import credentials, auth
from flask import Flask, request, jsonify, render_template
from functools import wraps
from settings import firebase_config, firebaseAdmin_config, flask_config


# Initialize Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = flask_config['SECRET_KEY']


# Initialize Firebase_admin and Pyrebase
cred = credentials.Certificate(firebaseAdmin_config)
firebase = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(firebase_config)
db = pb.database()


def check_token(f):
    """ Verify the validity of the Firebase Auth Token stored in the session cookie """
    @wraps(f)
    def wrap(*args,**kwargs):
        session_cookie = request.cookies.get('fbSession')
        if not session_cookie:
            return jsonify({'status': 'error', 'message': 'No token provided'}), 400

        try:
            user = auth.verify_session_cookie(session_cookie, check_revoked=True)
        except Exception as e:
            return jsonify({'status': 'error', 'message': 'Invalid token.'}), 400

        return f(user)
    return wrap


@app.route('/', methods=['GET'])
def index():
    """ Show the login and account registration form """
    return render_template('index.html', response=None)


@app.route('/signup', methods=['POST'])
def signup():
    """ Handle Firebase account creation """
    if request.method == 'POST':
        email = request.form.get('email')
        passwd = request.form.get('password')

        try:
            user = pb.auth().create_user_with_email_and_password(email, passwd)
            response = {'status': 'success', 'message': 'You can now login!'}
            return render_template('index.html', response=response)
        except Exception as e:
            response = {'status': 'error', 'message': 'Failed to creat account!'}
            return render_template('index.html', response=response)


@app.route('/login', methods=['POST'])
def login():
    """ Handle the login request with Firebase """
    if request.method == 'POST':
        email = request.form.get('email')
        passwd = request.form.get('password')
        expires_in = timedelta(hours=1)

        try:
            user = pb.auth().sign_in_with_email_and_password(email, passwd)
            id_token = user['idToken']
            session_cookie = auth.create_session_cookie(id_token, expires_in=expires_in)
            response = jsonify({'status': 'success', 'message': 'Logged in! Check user details on /private endpoint. /logout to log out.'})
            expires = datetime.now() + expires_in
            response.set_cookie('fbSession', session_cookie, expires=expires, httponly=True, secure=True)
            return response

        except Exception as e:
            response = { 'status': 'error', 'message': 'Email or Password invalid!'}
            return render_template('index.html', response=response)


@app.route('/logout', methods=['GET'])
def logout():
    """ Expire the session cookie, logging out the user """
    session_cookie = request.cookies.get('fbSession')
    if session_cookie:
        response = jsonify({'status': 'success', 'message': 'Logged out!'})
        response.set_cookie('fbSession', expires=0)
        return response


@app.route('/private')
@check_token
def private(user):
    """ Show user details if session cookie auth token is valid """
    return user
