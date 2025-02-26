import firebase_admin
from firebase_admin import credentials, firestore, auth
import os
import json
import base64

creds_base64 = os.getenv("GOOGLE_CLOUD_CREDENTIALS")

creds_json = json.loads(base64.b64decode(creds_base64))

with open("credentials.json", "w") as f:
    json.dump(creds_json, f)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()