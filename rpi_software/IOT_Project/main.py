# Import main python library for numerical calculations
import numpy as np
from PIL import Image, ImageDraw
# Import library for implementing delays
import time
# Import library for multi-threading
import threading

# Import various kivy libraries
import kivy
kivy.require('1.10.0')
from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.graphics import *
from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty
from kivy.uix.image import AsyncImage
from kivy.core.window import Window

# Import camera object for python
import cv2
# Specify the camera to use, 0 = built-in
cap = cv2.VideoCapture(0)

# Import
import cognitive_face as CF
file = open('keys.txt', 'r')
KEY = file.readline()
CF.Key.set(KEY)
BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

## Import firebase library
# import firebase_admin
# from firebase_admin import credentials, firestore
# cred = credentials.Certificate('')
# default_app = firebase_admin.initialize_app(cred)
# db = firestore.client


# Initialize global variables
global wait
wait = 4    # set rate (in seconds) for acquiring frames from camera
global QUIT
QUIT = True # boolean for terminating camera (maybe app)

##################################################
# Class which runs the functional GUI application.
##################################################
class ScreenOne(Screen):
    ##########################################################
    # This function runs when the class object is initialized
    # and ran (not 100% sure).
    ##########################################################
    def __init__(self, **kwargs):
        super(ScreenOne, self).__init__(**kwargs)

    ##############################################################
    # This is an event that is fired when the screen is displayed.
    ##############################################################
    def on_enter(self, *args):
        # Initialize a lock object -> haven't found reason to use
        # but its here in case :D
        global lock
        lock = threading.Lock()
        # Start a separate thread for user recognition
        global camera_thread
        #camera_thread = threading.Thread(target=self.acquireImage)
        #camera_thread.start()
        #camera_thread.join()
        # Start a separate thread for GUI
        global main_thread
        main_thread = threading.Thread(target=self.set_init_widgets)
        main_thread.start()
        main_thread.join()

    #######################################################
    # Function for acquiring images/frames from environment
    #######################################################
    def acquireImage(self):
        while True:
            # Code for waiting after frame (integer value to mili-seconds)
            time.sleep(wait)
            # Capture frame-by-frame
            ret, frame = cap.read()
            # Check if frame was successfully acquired
            if ret == True:
                # Our operations on the frame come here
                color_obj = cv2.cvtColor(frame, cv2.COLORMAP_BONE)
                # Write the frame into the file newImage.jpg
                cv2.imwrite('environment_image.png', color_obj)
                check = main_thread.isAlive()
                print(check)
                faces = CF.face.detect('environment_image.png')
                # Communicate with user faces database here
                #
                # If face is of a user, proceed to next stage
                # if face....
                #   # Call function changeTexts

                # self.center_image.source = 'newImage.png'


        # self.ids.label_1_sc1.color = 0,1,0,1
        # self.ids.label_1_sc1.text = "User Found..."

    ####################################################################
    # Use this function for changing the text parameters when a user has
    # been found via function acquireImage.
    ####################################################################
    @mainthread
    def changeTexts(self):
        # Disable category, go left, go right, and quit buttons at start
        self.ids.left_button.disabled = False
        self.ids.right_button.disabled = False
        self.ids.categ_button.disabled = False
        self.ids.quit_button.disabled = False
        # Set attributes of GUI widgets to use when user is found
        self.ids.categ_button.text = "Category:______"
        self.ids.categ_button.color = 1, 1, 0, 1
        self.ids.quit_button.text = "QUIT APP"
        self.ids.quit_button.color = 1, 0, 0, 1
        self.ids.left_button.text = "<"
        self.ids.right_button.text = ">"
        self.ids.timer_label.text = "0 sec"

    ###############################################################
    # Use this function for initializing the initial color, format,
    # and functionality of the GUI widgets
    ###############################################################
    @mainthread
    def set_init_widgets(self):
        # Initialize timer label to blank
        self.ids.timer_label.text = ""
        # Bind buttons on GUI to specific functions
        self.ids.left_button.bind(on_press=self.go_left)
        self.ids.right_button.bind(on_press=self.go_right)
        self.ids.quit_button.bind(on_press=self.quit_main)
        # Instantiate DropDown button
        global dropdown
        dropdown = CustomDropDown()
        self.ids.categ_button.bind(on_release=dropdown.open)
        # dropdown.bind(on_select=lambda instance, x: setattr(self.ids.categ_button, 'text', x))
        dropdown.bind(on_select=lambda instance,x: setattr(self.ids.categ_button, 'text', x))
        dropdown.bind(on_dismiss=lambda x: self.setUp_viewer_ads())
        # Disable category, go left, go right, and quit buttons at start
        self.ids.left_button.disabled = True
        self.ids.right_button.disabled = True
        self.ids.categ_button.disabled = False
        self.ids.quit_button.disabled = True

        # Clock.schedule_once(lambda dt: self.timer_label_count(0), 0)

    ####################################################################
    #
    #
    ####################################################################
    @mainthread
    def setUp_viewer_ads(self):
        print(self.ids.categ_button.text)
        self.ids.center_image.source = 'newImage.png'

    ####################################################################
    #
    #
    ####################################################################
    @mainthread
    def timer_label_count(self,num):
        if num == 10:
            self.ids.timer_label.color = 1, 0, 0, 1
            self.ids.timer_label.text = str(num)
            return
        num += 1
        self.ids.timer_label.text = str(num)
        Clock.schedule_once(lambda dt: self.timer_label_count(num), 1)

    #############################################################
    # Function for implementing an action when the user presses
    # the left arrow.
    # - Make left ad appear (could be end image on opposite end).
    #############################################################
    @mainthread
    def go_left(self):
        pass

    #############################################################
    # Function for implementing an action when the user presses
    # the right arrow.
    # - Make right ad appear (could be first image on opposite end/direction).
    #############################################################
    @mainthread
    def go_right(self):
        pass

    #############################################################
    # Function for when the user presses the QUIT button.
    #############################################################
    @mainthread
    def quit_main(self):
        # Disable category, go left, go right, and quit buttons at start
        self.ids.left_button.disabled = True
        self.ids.right_button.disabled = True
        self.ids.categ_button.disabled = True
        self.ids.quit_button.disabled = True
        # Set attributes of GUI widgets to use when user is found
        self.ids.categ_button.text = ""
        self.ids.categ_button.color = 0, 0, 0, 1
        self.ids.quit_button.text = ""
        self.ids.quit_button.color = 0, 0, 0, 1
        self.ids.left_button.text = ""
        self.ids.right_button.text = ""
        self.ids.timer_label.text = ""

#############################################################
# This class is used to connect to the kivy class of the same
# name. The kivy class is used to create a drop menu for
# letting the user select from a variety of advertisements.
#############################################################
class CustomDropDown(DropDown):
    pass

#############################################################
# This class is for instantiating an initial screen to use.
# Intended to be used when the GUI was going to be multiple
# screens versus the current 1 screen.
#############################################################
class Manager(ScreenManager):
    stop = threading.Event()
    screen_one = ObjectProperty(None)

#############################################################
# Separate class for running the kivy GUI.
#############################################################
class ScreensApp(App):
    # NOT REALLY IMPLEMENTED... YET.
    def on_stop(self):
        # The Kivy event loop is about to stop, set a stop signal;
        #  otherwise the app window will close, but the Python process will
        # keep running until all secondary threads exit.
        self.root.stop.set()
    # Start the program
    def build(self):
        m = Manager(transition=NoTransition())
        return m

# Runs program -> NOT PART OF ANY CLASS!
if __name__ == "__main__":
    ScreensApp().run()
