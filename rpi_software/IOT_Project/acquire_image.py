import numpy as np
import cv2

cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Unable to read camera feed")

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
# out = cv2.VideoWriter('outpy.png', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))
# Alternative method for singular frame, where img is the frame
# cv2.imwrite('newImage.png', img)

ii = 1
# max = 10
wait = 1

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret == True:
        # Write the frame into the file 'output.avi'
  #      out.write(frame)

        # Our operations on the frame come here
        color_obj = cv2.cvtColor(frame, cv2.COLORMAP_BONE)

        # Display the resulting frame
        cv2.imshow('frame',color_obj)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # Code for waiting after frame (integer value to mili-seconds)
        cv2.waitKey(wait)
    # Break the loop
    else:
        break

# When everything done, release the capture
cap.release()
# out.release()
cv2.destroyAllWindows()

# Source for code:
# https://www.learnopencv.com/read-write-and-display-a-video-using-opencv-cpp-python/
# https://kivy.org/docs/api-kivy.uix.videoplayer.html
# https://kivy.org/docs/api-kivy.uix.image.html