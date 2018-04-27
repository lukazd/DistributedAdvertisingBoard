# Import library for implementing delays
import json
import time
import urllib.error
import urllib.parse
import http
import cognitive_face as CF
import cv2
from PIL import Image, ImageDraw
import requests

# Specify the camera to use, 0 = built-in
cap = cv2.VideoCapture(0)

# Replace with a valid subscription key (keeping the quotes in place).
file = open('keys.txt', 'r')
print(file.readline())
KEY = file.readline()
CF.Key.set(KEY)
# Initialize the group name to save
global mcg_group_name
mcg_group_name = "large-person-group-dev"

# Replace with your regional Base URL
BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'
CF.BaseUrl.set(BASE_URL)
#CF.large_person_group.train(mcg_group_name)

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Unable to read camera feed")

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
# frame_width = int(cap.get(3))
# frame_height = int(cap.get(4))

ii = 0
max = 1
wait = 2

while(ii < max ):
    # Code for waiting after frame (integer value to mili-seconds)
    time.sleep(wait)

    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret == True:
        # Our operations on the frame come here
        color_obj = cv2.cvtColor(frame, cv2.COLORMAP_BONE)
        # Write the frame into the file newImage.jpg
        cv2.imwrite('environment_image.png', color_obj)
        CF.util.wait_for_large_person_group_training(mcg_group_name)
        faces = CF.face.detect('environment_image.png')
        #faces = CF.face.detect('environment_image.png')[]['faceId']
        #print(faces)
        #print(CF.face.identify([faces], large_person_group_id=mcg_group_name))
        ii = 0
        for face in faces:
            faceID = faces[ii]['faceId']
            print(CF.face.identify([faceID], large_person_group_id=mcg_group_name))
            temp = CF.face.identify([faceID], large_person_group_id=mcg_group_name)

            if len(temp[0]["candidates"]) != 0:
                print(temp[0]["candidates"][0]['personId'])
            ii = ii + 1
         # image_data = open('environment_image.png', "rb").read()

        # Convert width height to a point in a rectangle
        def getRectangle(faceDictionary):
            rect = faceDictionary['faceRectangle']
            left = rect['left']
            top = rect['top']
            bottom = left + rect['height']
            right = top + rect['width']
            return ((left, top), (bottom, right))


        # Download the image from the url
        # response = cv2.imread('newImage.jpg')
        # img = Image.open(BytesIO(cv2.imread('newImage.jpg')))
        img = Image.open('environment_image.png')

        # For each face returned use the face rectangle and draw a red box.
        draw = ImageDraw.Draw(img)
        one_face = None
        for face in faces:
            #draw.rectangle(getRectangle(face), outline='red')
            one_face = face

        # Display the image in the users default image browser.
        img2 = img.crop((getRectangle(one_face)[0][0] - 40, getRectangle(one_face)[0][1] - 75,
                         getRectangle(one_face)[1][0] + 40, getRectangle(one_face)[1][1] + 30))
        #img.show()
        img2.save("temp_img2.jpg")
        img2.show()
        ii = ii + 1
        break


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()