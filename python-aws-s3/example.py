import os
import boto3
from botocore.client import Config

ACCESS_KEY_ID = 'AKIAJEGS5FI3IGU3UI7A'
ACCESS_SECRET_KEY = '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'
BUCKET_NAME = 'upload-valid-temp-images'

data = open('target1.jpg', 'rb')

s3 = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY,
    config=Config(signature_version='s3v4')
)
s3.Bucket(BUCKET_NAME).put_object(Key='target1.jpg', Body=data)

print ("Done")

os.system('python list-bucket.py')
#import boto3
#from botocore.client import Config
