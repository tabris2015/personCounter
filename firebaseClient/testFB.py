
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
cred = credentials.Certificate('key2.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

eventos_ref = db.collection(u'eventos')

docs = eventos_ref.get()

for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))
