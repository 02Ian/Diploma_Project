import boto3
from botocore.client import Config

client = boto3.client('rekognition',region_name='ap-south-1')
response = client.compare_faces(
SourceImage={
'S3Object': {
'Bucket': 'upload-valid-images',
'Name': 'Source1.jpg'
}
},
TargetImage={
'S3Object': {
'Bucket': 'upload-valid-temp-images',
'Name': 'target1.jpg'
}
},

)
print(response)
    