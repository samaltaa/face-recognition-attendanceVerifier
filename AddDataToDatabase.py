import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# reference the json file
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://facedata-3a93d-default-rtdb.firebaseio.com/"
})
# database reference to data
ref = db.reference("Employees")

data = {
    # this is a key and everything within is the value
    "963852":
        {
            "Name": "Elon Musk",
            "Position": "Oligarch",
            "Starting Year": "2010",
            "Total Attendance": 794,
            "Standing": "Probationary",
            "Year": 9,
            "Last Attendance Time": "07/13/2023 00:59:34"
        }
}

# push data to database
for key,value in data.items():
    # for sending data to a specific directory you have to use child()
    ref.child(key).set(value)