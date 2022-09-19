# Flask / Firebase Authentication with Session Cookies

![Firebase Logo](fb_logo.png)
[https://firebase.google.com/](https://firebase.google.com/)

## Setup
* Copy the `dotEnvExample` file to `.env`.
* Create a Firebase project and register your app: https://firebase.google.com/docs/web/setup  
* In the Firebase Console, go to Project Settings and find the app settings. Populate the `.env` file with the values.
* Under Project Settings, go to "Service Account" and generate a new key. Open the JSON file and populate the `.env` file with the values.


## Usage
* Install the dependencies: `python3 pip install -r requirements.txt`  
* Run the application: `python3 app.py`
* Open a browser: `http://localhost:8000`
* Register a user account
* Login with the account and head to `/private` afterwards, you'll see the firebase user object.
* Logout by requesting the `/logout` path. Try to open the `/private` endpoint again.
