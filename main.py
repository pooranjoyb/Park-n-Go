from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

#Set pre defined window size
Window.size = (600, 600)
class Screen(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("./Components/screen.kv"))
        return screen_manager

Screen().run()


                
        

        