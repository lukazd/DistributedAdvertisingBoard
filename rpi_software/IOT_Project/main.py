import numpy as np
import cv2
from PIL import Image, ImageDraw
import cognitive_face as CF
import time
import threading
import firebase_admin
from firebase_admin import credentials, firestore

import kivy
kivy.require('1.10.0')
#import Clock to create a schedule
from kivy.clock import Clock
from kivy.app import App
from kivy.lang import Builder
from kivy.graphics import *
from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.image import AsyncImage
from kivy.core.window import Window

# Loading images asycnhorously:
# https://kivy.org/docs/api-kivy.uix.image.html#kivy.uix.image.AsyncImage

# Example of dynamic screen manager
# https://stackoverflow.com/questions/34787525/kivy-changing-screen-from-python-code


# Specify the camera to use, 0 = built-in
cap = cv2.VideoCapture(0)

KEY = 'bead87ccbe074693a5a793d101c8086d'
#KEY = 'b7ae1171b8ad4b68b3839034902418ec'
CF.Key.set(KEY)
BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

# cred = credentials.Certificate('')
# default_app = firebase_admin.initialize_app(cred)
# db = firestore.client

global wait
wait = 4000
global QUIT
QUIT = 1

class ScreenOne(Screen):

    def __init__(self, **kwargs):
        super(ScreenOne, self).__init__(**kwargs)

    #this is event that is fired when the screen is displayed.
    def on_enter(self, *args):
        # Initialize a lock object
        global lock
        lock = threading.Lock()

        # Start a separate thread for user recognition

        # Change the various labels
        # self.
        # self.acquireImage()
        pass

    def displayScreenThenLeave(self):
        pass
        # schedued after 3 seconds

        # Clock.schedule_once(self.changeScreen, 4)
        # Clock.schedule_once(self.acquireImage, 4)

    def acquireImage(self):
        check_photo = 1

        while(QUIT == 1):
            # Capture frame-by-frame
            ret, frame = cap.read()
            if ret == True:
                # Our operations on the frame come here
                color_obj = cv2.cvtColor(frame, cv2.COLORMAP_BONE)
                # Write the frame into the file newImage.jpg
                cv2.imwrite('newImage.png', color_obj)
                # faces = CF.face.detect('newImage.jpg')
                # Communicate with user faces database here
                #
                # If face is of a user, proceed to next stage
                # if face....
                #   # Call function changeTexts

                # self.center_image.source = 'newImage.png'

            # Code for waiting after frame (integer value to mili-seconds)
            cv2.waitKey(wait)

        # self.ids.label_1_sc1.color = 0,1,0,1
        # self.ids.label_1_sc1.text = "User Found..."

    def changeTexts(self):
        self.ids.categ_button.text = "Category:______"
        self.ids.categ_button.color = 0.54,0.824,1, 1
        self.ids.quit_button.text = "Quit"
        self.ids.quit_button.color = 1, 0, 0, 1
        self.ids.left_button.text = "<"
        self.ids.right_button.text = ">"
        self.ids.timer_label.text = "0 sec"

    def set_init_widgets(self):
        # self.ids.
        pass

class Manager(ScreenManager):

    screen_one = ObjectProperty(None)
    screen_two = ObjectProperty(None)
    screen_three = ObjectProperty(None)

class ScreensApp(App):

    def build(self):
        m = Manager(transition=NoTransition())
        return m

if __name__ == "__main__":
    ScreensApp().run()
