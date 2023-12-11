import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json") #credentials
firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://faceantendancerealtime-default-rtdb.firebaseio.com/' #From Real time database

})
# Table called Students
ref = db.reference('Students')
data = {
    '217051340':
    {
        'name':'NTAMBARA Etienne',
        'major':'Machine Learning',
        'qualification': 'MScAI',
        'starting_year': 2023,
        'total_attendance':6,
        'standing':'G',
        'year':4,
        'last_attendance_time': '2023-11-29 00:54:34'
    },
        '217051341':
    {
        'name':'HATEGEKA Emmy',
        'major':'Computer Science',
        'qualification': 'BScSC',
        'starting_year': 2021,
        'total_attendance':4,
        'standing':'M',
        'year':4,
        'last_attendance_time': '2022-11-28 00:54:34'
    },
        '217051342':
    {
        'name':'UWINEZA Joseph',
        'major':'Computer Vision',
        'qualification': 'MScAI',
        'starting_year': 2023,
        'total_attendance':5,
        'standing':'G',
        'year':4,
        'last_attendance_time': '2023-11-30 00:54:34'
    }
}

# send data to database
for key,value in data.items():
    ref.child(key).set(value)

