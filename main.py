from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

#Set pre defined window size
Window.size = (600, 600)
class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()

class Screen(MDApp):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("./Components/screen.kv"))
        screen_manager.add_widget(Builder.load_file("./Components/login.kv"))
        return screen_manager

if __name__=="__main__":
    LabelBase.register(name="MPoppins", fn_regular="assets/fonts/Poppins-Medium.ttf")
    LabelBase.register(name="BPoppins", fn_regular="assets/fonts/Poppins-SemiBold.ttf")
Screen().run()


                
        

        