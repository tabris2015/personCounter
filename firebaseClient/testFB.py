import pyrebase
config = {
  "apiKey": "AIzaSyCZD5p33MawUzTc-amsrQhnbRe0mZpMEvo",
  "authDomain": "asobancontrolferia.firebaseapp.com",
  "databaseURL": "https://asobancontrolferia.firebaseio.com",
  "storageBucket": "asobancontrolferia.appspot.com",
  "serviceAccount": "key2.json"
}
firebase = pyrebase.initialize_app(config)

db = firebase.database()
data = {"name": "pepe"}
db.child("test").set(data)
users = db.child("test").get()
print users.val()