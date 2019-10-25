import boto3
from botocore.client import Config

s3 = boto3.resource('s3')
src_bucket = s3.Bucket('upload-valid-images')
# Iterates through all the objects, doing the pagination for you. Each obj
# is an ObjectSummary, so it doesn't contain the body. You'll need to call
# get to get the whole body.
source= []
for obj in src_bucket.objects.all():
    source.append(obj.key)
print(source)
trgt_bucket = s3.Bucket('upload-valid-temp-images')
target= []
for obj in trgt_bucket.objects.all():
    target.append(obj.key)
print(target)

client = boto3.client('rekognition',region_name='ap-south-1')
response = []
for x in source:
	response.append(client.compare_faces(
	   SourceImage={
	      'S3Object': {
	      'Bucket': 'upload-valid-images',
	      'Name': x
	      }
	   },
	   TargetImage={
	      'S3Object': {
	      'Bucket': 'upload-valid-temp-images',
	      'Name': 'target1.jpg'
	      }
	   }
	))

# print response
res_len = (len(response))
res_len = res_len -1

# face=response['FaceMatches']
# # print (face)
# for record in response['FaceMatches']:
#    face = record
#    confidence=face['Face']
#    print ("Matched With {}"g"%"" Similarity".format(face['Similarity']))
#    print ("With {}""%"" Confidence".format(confidence['Confidence']))
# for x in response:
#     print(x['ResponseMetadata']['UnmatchedFaces'])

while res_len >=0:
    if(response[res_len]['FaceMatches'] <> []):
        print(response[res_len]['FaceMatches'][0]['Similarity'])
    res_len = res_len - 1
