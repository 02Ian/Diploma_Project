import os
#import cv2

# cam = cv2.VideoCapture(0)
# ret, frame = cam.read()
# img_name = "target.png"
# cv2.imwrite(img_name, frame)
# print("{} written!".format(img_name))
#
#
# cam.release()
#
# cv2.destroyAllWindows()

os.system('fswebcam target1.jpg')
os.system('python example.py')
print('call successfully returns to the calling pythin file')
