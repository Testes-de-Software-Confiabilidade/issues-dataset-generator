import os
from firebase import Firebase
from dotenv import load_dotenv
load_dotenv()


config = {
    "apiKey": os.environ.get("apiKey", None),
    "authDomain": os.environ.get("authDomain", None),
    "databaseURL": os.environ.get("databaseURL", None),
    "projectId": os.environ.get("projectId", None),
    "storageBucket": os.environ.get("storageBucket", None),
    "messagingSenderId": os.environ.get("messagingSenderId", None),
    "appId": os.environ.get("appId", None)
}

# print(config)

firebase = Firebase(config)
db = firebase.database()
print(db.child("processing_urls").get())