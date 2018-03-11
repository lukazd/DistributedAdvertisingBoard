import numpy as np
import cv2
import kivy
import threading
kivy.require('1.10.0')
#import Clock to create a schedule
from kivy.clock import Clock
from kivy.app import App
from kivy.lang import Builder
from kivy.graphics import *
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty, NumericProperty
from kivy.core.window import Window

# Loading images asycnhorously:
# https://kivy.org/docs/api-kivy.uix.image.html#kivy.uix.image.AsyncImage

# Example of dynamic screen manager
# https://stackoverflow.com/questions/34787525/kivy-changing-screen-from-python-code

class ScreenOne(Screen):

    def __init__(self, **kwargs):
        super(ScreenOne, self).__init__(**kwargs)

    #this is event that is fired when the screen is displayed.
    def on_enter(self, *args):
        self.displayScreenThenLeave()

    def displayScreenThenLeave(self):
        #schedued after 3 seconds
        Clock.schedule_once(self.changeScreen, 3)

    def changeScreen(self, *args):
        #now switch to the screen 1
        self.parent.current = "screen2"

class ScreenTwo(Screen):
    def changeScreen(self):
        if self.manager.current == 'screen2':
            self.manager.current = 'screen3'
        else:
            self.manager.current = 'screen3'

class ScreenThree(Screen):
    def changeScreen(self):
        if self.manager.current == 'screen3':
            self.manager.current = 'screen1'
        else:
            self.manager.current = 'screen1'

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

# screen_manager = ScreenManager()
# screen_manager.add_widget(ScreenOne(name="screen_one"))
# screen_manager.add_widget(ScreenTwo(name="screen_two"))
# screen_manager.add_widget(ScreenThree(name="screen_three"))
#
# class RunGUI_App(App):
#
#     def build(self):
#         return screen_manager
#
# sample_app = RunGUI_App()
# Window.fullscreen = True

# Builder.load_string("""
# <ScreenOne>:
#     BoxLayout:
#         orientation: 'vertical'
#         Label:
#             id: lab_rec1
#             text: "Rec"
#             size_hint: 0.3, .3
#             font_size: 20
#             font_weight: "Bold"
#             color: 1, 0, 0, 1
#             pos_hint: {'left': 0.2 + self.size_hint[1]/2}
#             canvas:
#                 Color:
#                     rgb: 1, 0, 0
#                 Ellipse:
#                     pos: 10,10
#                     size: 10, 10
#
#         Button:
#             background_normal: ''
#             background_color: 0, 0, 0, 1
#             text: "Distributed Advertising Board"
#             font_size: 50
#             font_weight: "Bold"
#             center: self.parent.center
#             pos_hint: {'top': 0.2 + self.size_hint[1]/2}
#             on_press:
#                 root.manager.current = "screen_two"
# <ScreenTwo>:
#     GridLayout:
#         orientation: 'vertical'
#         Label:
#             text: ""
#         Label:
#             text: ""
#         Button:
#             text: "View Ads?"
#             on_press:
#                 root.manager.current = "screen_three"
# <ScreenThree>:
#     BoxLayout:
#         orientation: 'horizontal'
#         Button:
#             text: "<"
#         Label:
#             text: ""
#         Button:
#             text: ">"
#
# """)