from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen

#Set pre defined window size
Window.size = (600, 600)


class WindowManager(ScreenManager):
    pass

class Park(MDApp):
    def build(self):
        self.screen = Builder.load_file("./Components/main.kv")
        return self.screen

    def hello(self):
        print(self.screen.get_screen('login').ids.text1.text)
        print(self.screen.get_screen('login').ids.passw.text)

if __name__=="__main__":
    LabelBase.register(name="MPoppins", fn_regular="assets/fonts/Poppins-Medium.ttf")
    LabelBase.register(name="BPoppins", fn_regular="assets/fonts/Poppins-SemiBold.ttf")
Park().run()


                
        

        