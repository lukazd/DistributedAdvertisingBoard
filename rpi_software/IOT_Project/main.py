import json
import sys, os
import requests
import urllib, urllib3
import time
import threading
import cv2
import kivy

import cognitive_face as CF
import numpy as np

from kivy.app import App
from kivy.cache import Cache
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
from kivy.graphics.texture import Texture
from PIL import Image, ImageDraw
from functools import partial

urllib3.disable_warnings()
kivy.require('1.10.0')

######################### Microsoft Cognitive ###############################
global mcg_group_name
mcg_group_name = "large-person-group-dev"
KEY = os.environ['COG_KEY']
CF.Key.set(KEY)
BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

#img_path = os.path.join(os.path.curdir, 'environment_image.png')
################### Initialize global variables ##############################

class SenseAdEndpoint():
    URL = "http://sensead.westcentralus.cloudapp.azure.com:8000"
    GET_ADS_PATH = "/getAdsForUser?user_id="
    RATE_AD_PATH = "/rateAd"
    LOG_OUT_PATH = "/logOut"

class CapturedFrame():
    def __init__(self, frame):
        self.frame = frame

    def read(self):
        png_image = cv2.imencode('.png', self.frame)[1]
        return bytes(bytearray(png_image.tostring()))

    def texture(self):
        buf = cv2.flip(self.frame, 0).tostring()
        image_texture = Texture.create(size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        return image_texture

class ScreenOne(Screen):

    def __init__(self, **kwargs):
        super(ScreenOne, self).__init__(**kwargs)
        self.camera_thread = threading.Thread(target=self.acquireImage)
        self.wait = 3
        self.quit = True
        self.response_json = None
        self.ad_counter = 0
        self.timer_stop = 0
        self.payment = 0

    def spawn_camera_thread(self):
        self.camera_thread = threading.Thread(target=self.acquireImage)
        self.camera_thread.setDaemon(True)
        self.camera_thread.start()

    def on_enter(self, *args):
        self.set_init_widgets()
        self.spawn_camera_thread()

    def getRectangle(self, faceDictionary):
        rect = faceDictionary['faceRectangle']
        left = rect['left']
        top = rect['top']
        bottom = left + rect['height']
        right = top + rect['width']
        return ((left, top), (bottom, right))

    def acquireImage(self):
        # State global variables
        cap = cv2.VideoCapture(0)

        while True:
            # Code for waiting after frame (integer value to milli-seconds)
            time.sleep(self.wait)

            if self.quit == True:
                ret, frame = cap.read()

            # Check if frame was successfully acquired
            if ret == True:
                face_image = CapturedFrame(frame)

                faces = CF.face.detect(face_image)
                for face in faces:
                    identities = CF.face.identify([face['faceId']], large_person_group_id=mcg_group_name)[0]["candidates"]

                    if len(identities) > 0:
                        ad_request_url = SenseAdEndpoint.URL + SenseAdEndpoint.GET_ADS_PATH + identities[0]['personId']
                        contents = requests.get(ad_request_url)
                        self.response_json = contents.json()
                        self.quit = False
                        self.user_found(face, face_image)
                        cap.release()
                        return

    @mainthread
    def user_found(self, face, face_image):
        self.ad_counter = 0
        self.payment = 0
        userName = self.response_json["person"]["personName"]
        self.ids.user_label.color = 0, 1, 0, 1
        self.ids.user_label.text = "Hello, " + userName + '.'
        #img = Image.open(img_path)
        #img2 = img.crop((self.getRectangle(face)[0][0] - 40, self.getRectangle(face)[0][1] - 75,
        #                 self.getRectangle(face)[1][0] + 40, self.getRectangle(face)[1][1] + 30))
        #img2.save("temp_img2.png")
        #self.ids.user_image.source = ""
        #self.ids.user_image.source = "temp_img2.png"
        self.ids.user_image.texture = face_image.texture()
        #self.ids.user_image.reload()
        #self.ids.user_image.source = ""
        self.ids.center_image.source = self.response_json["ads"][self.ad_counter]["ad"]["url"]
        self.change_texts()

    @mainthread
    def help_popup(self):
        #TODO: Fix this string
        help_text = (
            'This is the SenseAd Kiosk. If you have registered through the app then the kiosk '
            'will be able to identify you. When prompted, select a category of ads to view. '
            'A timer will be on to indicate if you have viewed the ad for enough time (~10 seconds).\n'
        )
        button_text = 'Press to close me!'
        content = BoxLayout()
        popup_help = Popup(title='Help Page', content=content, auto_dismiss=True, size_hint=[0.7, 0.7])

        label = Label(
            text=help_text,
            background_normal='',
            background_color=[0, 0, 0, 1],
            text_size: self.size,
            halign: 'right',
            valign: 'middle'
        )

        content.add_widget(label)
        popup_help.open()

    @mainthread
    def change_texts(self):
        self.ids.like_button.disabled = True
        self.ids.dislike_button.disabled = True
        self.ids.neutral_button.disabled = True
        self.ids.quit_button.disabled = False

        self.ids.quit_button.text = "Log Out"
        self.ids.quit_button.color = 1, 1, 1, 1
        self.ids.timer_label.text = "0s"
        self.ids.like_button.text = "Like"
        self.ids.like_button.color = 0, 1, 0, 0.5
        self.ids.dislike_button.text = "Dislike"
        self.ids.dislike_button.color = 1, 0, 0, 0.5
        self.ids.neutral_button.text = "Neutral"
        self.ids.neutral_button.color = 0, 0.75, 1, 0.5

        self.timer_stop=True
        self.disable_pref_buttons()
        self.start_ad_timer()

    @mainthread
    def set_init_widgets(self):
        self.timer_stop=False
        self.ids.timer_label.text = ""

        self.ids.help_button.bind(on_release=lambda *args: self.help_popup())
        self.ids.like_button.bind(on_press=lambda *ads: self.pref_ads('Like'))
        self.ids.dislike_button.bind(on_press=lambda *ads: self.pref_ads('Dislike'))
        self.ids.neutral_button.bind(on_press=lambda *ads: self.pref_ads('Neutral'))
        self.ids.quit_button.bind(on_press=lambda *args: self.begin_log_out())

        self.ids.like_button.disabled = True
        self.ids.dislike_button.disabled = True
        self.ids.neutral_button.disabled = True
        self.ids.quit_button.disabled = True

    @mainthread
    def enable_pref_buttons(self):
        self.ids.like_button.disabled = False
        self.ids.like_button.color = 0, 1, 0, 1
        self.ids.dislike_button.disabled = False
        self.ids.dislike_button.color = 1, 0, 0, 1
        self.ids.neutral_button.disabled = False
        self.ids.neutral_button.color = 0, 0.75, 1, 1

    @mainthread
    def disable_pref_buttons(self):
        self.ids.like_button.disabled = True
        self.ids.like_button.color = 0, 1, 0, 0.5
        self.ids.dislike_button.disabled = True
        self.ids.dislike_button.color = 1, 0, 0, 0.5
        self.ids.neutral_button.disabled = True
        self.ids.neutral_button.color = 0, 0.75, 1, 0.5

    @mainthread
    def timer_label_count(self, num, *args):
        if self.timer_stop == True:
            self.ids.timer_label.text = str(num)+'s'
            if num == 0:
                self.ids.timer_label.color = 1, 0, 0, 1
                self.enable_pref_buttons()
            else:
                self.ids.timer_label.color = 0, 1, 0, 1

    @mainthread
    def resize_screen(self):
        Window.fullscreen = 'auto'

    @mainthread
    def pref_ads(self, opin_ad):
        self.payment += 1
        r = requests.post(SenseAdEndpoint.URL + SenseAdEndpoint.RATE_AD_PATH, data={'user_id' : self.response_json["person"]["personId"], 'ad_id' : self.response_json["ads"][self.ad_counter]['ad_id'], 'rating': opin_ad})
        print(r.content)

        self.disable_pref_buttons()
        self.ad_counter += 1

        if (len(self.response_json["ads"]) > self.ad_counter):
            self.ids.center_image.source = self.response_json["ads"][self.ad_counter]["ad"]["url"]
            self.ids.center_image.reload()
            self.start_ad_timer()
        else:
            self.begin_log_out()

    def start_ad_timer(self):
        self.ids.timer_label.color = 0, 1, 0, 1
        time.sleep(0.5)

        for i in range(10, -1, -1):
            Clock.schedule_once(partial(self.timer_label_count, i), 10-i)

    @mainthread
    def popup_iota(self):
        popup_text = 'Logging Out. You received an IOTA payment of ' + str(self.payment)
        content = Label( text=popup_text,            
                        background_normal='',
                        background_color=[0, 0, 0, 1],
                        text_size: self.size,
                        halign: 'right',
                        valign: 'middle')
        popup = Popup(title='IOTA Payment', content=content, auto_dismiss=True,
                      size_hint=(None, None), size=(300, 100))
        content.bind(on_release=popup.dismiss)
        popup.bind(on_dismiss=self.quit_main)
        popup.open()

    def begin_log_out(self):
        self.popup_iota()

    @mainthread
    def quit_main(self, args):
        r = requests.post(SenseAdEndpoint.URL + SenseAdEndpoint.LOG_OUT_PATH, data={'user_id' : self.response_json["person"]["personId"], 'payment' : self.payment})
        self.ids.center_image.source = 'background.jpg'
        self.ids.user_image.source = 'background.jpg'
        self.ids.user_image.reload()

        self.ids.like_button.disabled = True
        self.ids.dislike_button.disabled = True
        self.ids.neutral_button.disabled = True
        self.ids.quit_button.disabled = True

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

        self.timer_stop = False
        self.ids.timer_label.text = ""
        self.quit = True
        self.spawn_camera_thread()

class Manager(ScreenManager):
    stop = threading.Event()
    screen_one = ObjectProperty(None)

class ScreensApp(App):
    def on_stop(self):
        #self.root.stop.set()
        print("exited")

    # Start the program
    def build(self):
        m = Manager(transition=NoTransition())
        return m

if __name__ == "__main__":
    ScreensApp().run()
