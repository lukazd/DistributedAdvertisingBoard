# Import Libraries
import json
import os
import requests
import numpy as np
from PIL import Image, ImageDraw
import urllib
import urllib3
urllib3.disable_warnings()
# Import library for implementing delays
import time
# Import library for multi-threading
import threading

# Import various kivy libraries
import kivy
kivy.require('1.10.0')
from kivy.app import App
from kivy.cache import Cache
#Cache._categories['kv.image']['limit'] = 1
#Cache._categories['kv.image']['timeout'] = 1
#Cache._categories['kv.texture']['limit'] = 1
#Cache._categories['kv.texture']['timeout'] = 1
from kivy.clock import Clock, mainthread
from kivy.graphics import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty
from kivy.uix.image import AsyncImage
from kivy.core.window import Window
from kivy.config import Config
#from kivy.loader import Loader
#from kivy.core.image import ImageLoader
#from kivy.uix.image import Image
Config.set('graphics', 'fullscreen', 1)
# Import camera object for python
import cv2
# Specify the camera to use, 0 = built-in
cap = cv2.VideoCapture(0)

######################### Microsoft Cognitive ###############################
#### Import cognitive library ####
import cognitive_face as CF
# Initialize the group name to save
global mcg_group_name
mcg_group_name = "large-person-group-dev"
# Read subscription key from environment variable
KEY = os.environ['COG_KEY']
CF.Key.set(KEY)
# Set the base url to use (i.e. central USA)
BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

# Initialize name of image to save
img_path = 'environment_image.png'
global back_end_url
global my_json
back_end_url = "http://sensead.westcentralus.cloudapp.azure.com:8000/getAdsForUser?user_id="
back_end_url = "http://sensead.westcentralus.cloudapp.azure.com:8000/getAdsForUser?user_id=11bc97c4-657c-43bd-9852-8a95b192b0be"
################### Initialize global variables ##############################
wait = 3    # set rate (in seconds) for acquiring frames from camera
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
        # Start a separate thread for GUI
        #main_thread = threading.Thread(target=self.set_init_widgets)
        #main_thread.start()
        #main_thread.join()
        self.set_init_widgets()
        #contents = requests.get(back_end_url)
        #global my_json
        #my_json = contents.json()
        #QUIT = False
        #self.user_found()
        # Start a separate thread for user recognition
        camera_thread = threading.Thread(target=self.acquireImage)
        camera_thread.start()

    #######################################################
    # Function for converting width height to a point in
    # a rectangle. Used to outline user's face on screen.
    #######################################################
    def getRectangle(self, faceDictionary):
        rect = faceDictionary['faceRectangle']
        left = rect['left']
        top = rect['top']
        bottom = left + rect['height']
        right = top + rect['width']
        return ((left, top), (bottom, right))

    #######################################################
    # Function for acquiring images/frames from environment
    #######################################################
    def acquireImage(self):
        # State global variables
        global QUIT, wait

        while True:
            # Code for waiting after frame (integer value to milli-seconds)
            time.sleep(wait)

            # Check if a user is currently using the app
            # Capture frame-by-frame
            if QUIT == True:
                ret, frame = cap.read()

            # Check if frame was successfully acquired
            if ret == True:
                # Our operations on the frame come here
                color_obj = cv2.cvtColor(frame, cv2.COLORMAP_BONE)
                # Write the frame into the file newImage.jpg
                cv2.imwrite(img_path, color_obj)
                #im = Image.open(img_path)
                #im.show()
                faces = CF.face.detect(img_path)
                ii = 0
                for face in faces:
                    # Get ID of face and check within large database to check for user
                    faceID = faces[ii]['faceId']
                    temp = CF.face.identify([faceID], large_person_group_id=mcg_group_name)
                    # Get identity of user
                    if len(temp[0]["candidates"]) != 0:
                        # Get the personID of the identified user and start main application
                        url_backend = back_end_url + temp[0]["candidates"][0]['personId']
                        contents = requests.get(url_backend)
                        global my_json
                        my_json = contents.json()
                        QUIT = False
                        self.user_found(face)
                        break  # Quit for-loop
                    else:
                        # Iterate to next user if not found
                        ii = ii + 1
            ret = False

    ####################################################################
    # Function for setting up the help button pop-up.
    ####################################################################
    @mainthread
    def user_found(self):
        #self.acquire_thread()
        global my_json, counter
        counter = 0
        userName = my_json["person"]["personName"]
        self.ids.user_label.color = 0, 1, 0, 1
        self.ids.user_label.text = "Hello, " + userName + '.'
        img = Image.open(img_path)
        img2 = img.crop((self.getRectangle(face)[0][0] - 40, self.getRectangle(face)[0][1] - 75,
                         self.getRectangle(face)[1][0] + 40, self.getRectangle(face)[1][1] + 30))
        img2.save("temp_img2.png")
        self.ids.user_image.source = ""
        self.ids.user_image.source = "temp_img2.png"
        #self.ids.user_image.source = ""
        self.ids.center_image.source = my_json["ads"][counter]["ad"]["url"]
        self.changeTexts()

    ####################################################################
    # Function for getting an advertisement
    ####################################################################
    # def get_ad_url(self):
    #     global my_json, counter
    #     temp_img = Image.open(requests.get(my_json["ads"][counter]["ad"]["url"], stream=True).raw)
    #     temp_img.save("temp_ad.png")
    #     #temp_img = Loader.image(requests.get(my_json["ads"][counter]["ad"]["url"], stream=True).raw)
    #     #temp_img.bind(on_load=self._image_loaded)
    #     counter = counter + 1
    #     return "temp_ad.png"

    ####################################################################
    # Function for setting up the help button pop-up.
    ####################################################################
    @mainthread
    def help_popup(self):
        text1 = 'This is the SenseAd Kiosk. If you have registered through the app then the kiosk'
        text2 = ' will be able to identify you. \nWhen prompted, select a category of ads to view.'
        text3 = ' A timer will be on to indicate if you have viewed the ad for enough time (~10 seconds).\n'
        button_text = 'Press to close me!'
        fulltext = text1 + text2 + text3 + button_text
        content = BoxLayout()
        popup_help = Popup(title='Help Page', content=content, auto_dismiss=False, size_hint=[0.7, 0.7])
        # Instantiate a button object to add to the popup
        button = Button(
            text=fulltext,
            background_normal='',
            background_color=[0, 0, 0, 1],
            on_release=popup_help.dismiss,
            on_press=lambda *args: self.resize_screen()
        )
        # Add button widget to set layout
        content.add_widget(button)
        popup_help.open()

    ####################################################################
    # Use this function for changing the text parameters when a user has
    # been found via function acquireImage.
    ####################################################################
    @mainthread
    def changeTexts(self):
        # Disable buttons at start
        self.ids.like_button.disabled = True
        self.ids.dislike_button.disabled = True
        self.ids.neutral_button.disabled = True
        self.ids.quit_button.disabled = False
        # Set attributes of GUI widgets to use when user is found
        self.ids.quit_button.text = "QUIT APP"
        self.ids.quit_button.color = 1, 1, 1, 1
        self.ids.timer_label.text = "0s"
        self.ids.like_button.text = "Like"
        self.ids.like_button.color = 0, 1, 0, 0.5
        self.ids.dislike_button.text = "Dislike"
        self.ids.dislike_button.color = 1, 0, 0, 0.5
        self.ids.neutral_button.text = "Neutral"
        self.ids.neutral_button.color = 0, 0.75, 1, 0.5
        time.sleep(0.5)
        # self.resize_screen()
        global timer_stop
        timer_stop=True
        self.enable_pref_buttons()
        #Clock.schedule_once(lambda dt: self.timer_label_count(0), 1)

    ###############################################################
    # Use this function for initializing the initial color, format,
    # and functionality of the GUI widgets
    ###############################################################
    @mainthread
    def set_init_widgets(self):
        # Set timer_stop to false
        global timer_stop
        timer_stop=False
        # Initialize timer label to blank
        self.ids.timer_label.text = ""
        # Bind buttons on GUI to specific functions
        self.ids.help_button.bind(on_release=lambda *args: self.help_popup())
        self.ids.like_button.bind(on_press=lambda *ads: self.pref_ads('Like'))
        self.ids.dislike_button.bind(on_press=lambda *ads: self.pref_ads('Dislike'))
        self.ids.neutral_button.bind(on_press=lambda *ads: self.pref_ads('Neutral'))
        self.ids.quit_button.bind(on_press=lambda *args: self.quit_main())
        # Disable category, go left, go right, and quit buttons at start
        self.ids.like_button.disabled = True
        self.ids.dislike_button.disabled = True
        self.ids.neutral_button.disabled = True
        self.ids.quit_button.disabled = True
        # Resize screen to max
        #time.sleep(0.5)
        #self.resize_screen()

    ####################################################################
    # Function for enabling the ad preference buttons.
    ####################################################################
    @mainthread
    def enable_pref_buttons(self):
        self.ids.like_button.disabled = False
        self.ids.like_button.color = 0, 1, 0, 1
        self.ids.dislike_button.disabled = False
        self.ids.dislike_button.color = 1, 0, 0, 1
        self.ids.neutral_button.disabled = False
        self.ids.neutral_button.color = 0, 0.75, 1, 1

    ####################################################################
    # Function for enabling the ad preference buttons.
    ####################################################################
    @mainthread
    def disable_pref_buttons(self):
        self.ids.like_button.disabled = True
        self.ids.like_button.color = 0, 1, 0, 0.5
        self.ids.dislike_button.disabled = True
        self.ids.dislike_button.color = 1, 0, 0, 0.5
        self.ids.neutral_button.disabled = True
        self.ids.neutral_button.color = 0, 0.75, 1, 0.5

    ####################################################################
    # Function for controlling the timer label text. Should change per
    # ad.
    ####################################################################
    @mainthread
    def timer_label_count(self, num):
        global timer_stop
        if timer_stop == True:
            # ADD A CHECK HERE IF EQUAL TO 5 (OR OTHER VALUE)
            if num == 10:
                self.ids.timer_label.color = 1, 0, 0, 1
                self.ids.timer_label.text = str(num)+'s'
                self.enable_pref_buttons()
                return
            num += 1
            self.ids.timer_label.color = 1, 1, 1, 1
            self.ids.timer_label.text = str(num)+'s'
            self.ids.timer_label.color = 0, 1, 0, 1
            #Clock.schedule_once(lambda dt: self.timer_label_count(num), 1)

    ###################################################################
    # Function for resizing the screen. Gets rid of graphic problems
    ###################################################################
    @mainthread
    def resize_screen(self):
        Window.fullscreen = 'auto'

    ###################################################################
    # Function for implementing an action for whenever the user
    # presses either of the like buttons.
    ###################################################################
    @mainthread
    def pref_ads(self, opin_ad):
        # Handle like button here - pass to IOTA
        # Pay customer in IOTA

        #  Call self.popup_iota()
        #self.popup_iota()

        # Disable buttons
        #self.disable_pref_buttons()
        global my_json, counter
        counter = counter + 1
        # Check if there are still ads
        if len(my_json["ads"][counter]["ad"]["url"]) != 0:
            # Set new image
            #self.ids.center_image.source = 'background.jpg'
            #time.sleep(0.5)
            #self.ids.center_image.source = ''
            #self.ids.center_image.reload()
            self.ids.center_image.source = my_json["ads"][counter]["ad"]["url"]
            self.ids.center_image.reload()
            #self.ids.center_image.reload()
        # Reset timer
        self.ids.timer_label.color = 0, 1, 0, 1
        time.sleep(0.5)
        Clock.schedule_once(lambda dt: self.timer_label_count(0), 1)

    #############################################################
    # Functions for calling and dismissing a popup to inform the
    # user that their IOTA transfer.
    #############################################################
    @mainthread
    def popup_iota(self):
        content = Button(text='IOTA Transaction Initiated.')
        popup = Popup(title='IOTA Payment', content=content, auto_dismiss=False,
                      size_hint=(None, None), size=(300, 100))
        # bind the on_press event of the button to the dismiss function
        content.bind(on_release=popup.dismiss)
        popup.open()

    #############################################################
    # Function for when the user presses the QUIT button.
    #############################################################
    @mainthread
    def quit_main(self):
        # Change center image
        self.ids.center_image.source = 'background.jpg'
        self.ids.user_image.source = 'background.jpg'
        # Disable buttons at start
        self.ids.like_button.disabled = True
        self.ids.dislike_button.disabled = True
        self.ids.neutral_button.disabled = True
        self.ids.quit_button.disabled = True
        # Set attributes of GUI widgets to use when user is found
        self.ids.quit_button.text = ""
        self.ids.quit_button.color = 0, 0, 0, 1
        self.ids.like_button.text = ""
        self.ids.like_button.color = 0, 0, 0, 1
        self.ids.dislike_button.text = ""
        self.ids.dislike_button.color = 0, 0, 0, 1
        self.ids.neutral_button.text = ""
        self.ids.neutral_button.color = 0, 0, 0, 1
        self.ids.timer_label.text = "    "
        self.ids.user_label.color = 1, 0, 0, 1
        self.ids.user_label.text = "Finding user..."
        global timer_stop
        timer_stop = False
        self.ids.timer_label.text = ""
        self.resize_screen()
        QUIT = True

#############################################################
# This class is for instantiating an initial screen to use.
# Intended to be used when the GUI was going to be multiple
# screens versus the current 1 screen.
#############################################################
class Manager(ScreenManager):
    stop = threading.Event()
    screen_one = ObjectProperty(None)

#############################################################
# Separate class for running the Kivy GUI.
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
