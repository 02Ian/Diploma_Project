import os
import boto3
from botocore.client import Config

ACCESS_KEY_ID = 'AKIAJUMEP3EX7J7JGV3Q'
ACCESS_SECRET_KEY = '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'
BUCKET_NAME = 'image-captured'


s3 = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY,
    config=Config(signature_version='s3v4')
)
print("Select Option to upload photo:")
print("Camera 'C'or'c'")
print("Location 'L'or'l'")
up_type = raw_input("C or L?")

print(up_type)
if (up_type == 'C' or up_type == 'c'):
    name = raw_input("Mention name of the user :")
    os.system('fswebcam {}.jpg'.format(name))
    file_name = '{}.jpg'.format(name)
    data = open(file_name, 'rb')
    s3.Bucket(BUCKET_NAME).put_object(Key=file_name, Body=data)

elif (up_type == 'L' or up_type == 'l'):
    print('[OPTIONAL] NAME THE IMAGE FILE AS PER THE USERNAME')
    path = raw_input("Image Path:")
    data = open('target1.jpg', 'rb')
    s3.Bucket(BUCKET_NAME).put_object(Key='rat.jpg', Body=data)

else:
    print("Something went Wrong!!")







# data = open('target1.jpg', 'rb')
# s3.Bucket(BUCKET_NAME).put_object(Key='target1.jpg', Body=data)

print ("Done")
