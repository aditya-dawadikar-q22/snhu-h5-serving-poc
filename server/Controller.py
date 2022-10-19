import firebase_admin
# from firebase_admin import storage
from google.cloud import storage
import datetime

cred_obj = firebase_admin.credentials.Certificate('/home/aditya/Desktop/SNHU/oppi-glidepath-dev-proj-4086-d3c6708c8ce4.json')
default_app = firebase_admin.initialize_app(cred_obj)

storage_client = storage.Client.from_service_account_json('/home/aditya/Desktop/SNHU/oppi-glidepath-dev-proj-4086-d3c6708c8ce4.json')

def get_signed_url_for_blob(bucket_name,file_name):
    # contentServingBucket = storage.bucket(bucket_name) 
    # some_blob = contentServingBucket.get_blob(file_name) 

    # print(file_name)

    bucket = storage_client.get_bucket(bucket_name)
    some_blob = bucket.get_blob(file_name)

    url = some_blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(minutes=10),
        method="GET",
    )

    return url