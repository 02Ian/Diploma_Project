import boto3
def face_comparision():
    client = boto3.client('rekognition')
    response = client.compare_faces(
        SourceImage={
            'S3Object': {
                'Bucket': 'upload-valid-images',
                'Name': 'source.jpg'
                }
            },
        TargetImage={
            'S3Object': {
                'Bucket':  'upload-valid-temp-images',
                'Name': 'target.jpg'
                }
            },
        SimilarityThreshold= 80
    )
    return response['SourceImageFace'], response['FaceMatches']
source_face, matches = face_comparision()

print "Source Face ({Confidence}%)".format(**source_face)
for match in matches:
	print "Target Face ({Confidence}%)".format(**match['Face'])
	print "  Similarity : {}%".format(match['Similarity'])

# for record in face_comparision():
#     face = record
#     confidence=face['Face']
#     print ("Matched With {}""%"" Similarity".format(face['Similarity']))
#     print ("With {}""%"" Confidence".format(confidence['Confidence']))
