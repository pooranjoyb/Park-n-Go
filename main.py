from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

#Set pre defined window size
Window.size = (600, 600)
class Screen(MDApp):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("./Components/screen.kv"))
        screen_manager.add_widget(Builder.load_file("./Components/login.kv"))
        return screen_manager

if __name__=="__main__":
    LabelBase.register(name="MPoppins", fn_regular="assets/fonts/Poppins-Medium.ttf")
    LabelBase.register(name="BPoppins", fn_regular="/home/madhurjya/Downloads/Poppins-SemiBold.ttf")
Screen().run()


                
        

        