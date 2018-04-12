import numpy as np
import cv2
import cognitive_face as CF
import requests
from io import BytesIO
from PIL import Image, ImageDraw

# Import library for implementing delays
import time

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Specify the camera to use, 0 = built-in
cap = cv2.VideoCapture(0)

# Replace with a valid subscription key (keeping the quotes in place).
# file = open('keys.txt', 'r')
# KEY = file.readline()
# KEY = 'bead87ccbe074693a5a793d101c8086d'
KEY = '5af6e0825d3b41119e86f1c9634bb3d5'
CF.Key.set(KEY)

# Replace with your regional Base URL
BASE_URL = 'https://westus.api.cognitive.microsoft.com/face/v1.0/'
CF.BaseUrl.set(BASE_URL)

# If you need to, you can change your base API url with:
# CF.BaseUrl.set('https://westcentralus.api.cognitive.microsoft.com/face/v1.0/')

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
        cv2.imwrite('newImage.jpg', color_obj)

        faces = CF.face.detect('newImage.jpg')

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
        img = Image.open('newImage.jpg')

        # For each face returned use the face rectangle and draw a red box.
        draw = ImageDraw.Draw(img)
        for face in faces:
            draw.rectangle(getRectangle(face), outline='red')

        # Display the image in the users default image browser.
        img.show()

        ii = ii + 1
        break


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()