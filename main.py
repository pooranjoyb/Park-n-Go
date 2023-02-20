from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivymd.uix.pickers import MDTimePicker

#Set pre defined window size
Window.size = (600, 600)

class WindowManager(ScreenManager):
    pass

class Park_n_Go(MDApp):
    def build(self):
        self.screen = Builder.load_file("./Components/main.kv")
        return self.screen

    def hello(self):
        print(self.screen.get_screen('login').ids.text1.text)
        print(self.screen.get_screen('login').ids.passw.text)

    def show_time_picker(self):
        '''Open time picker dialog.'''
        time_dialog = MDTimePicker()
        time_dialog.open()

    def saveTodb(self):
        print("Data saved to database")

if __name__=="__main__":
    LabelBase.register(name="MPoppins", fn_regular="assets/fonts/Poppins-Medium.ttf")
    LabelBase.register(name="BPoppins", fn_regular="assets/fonts/Poppins-SemiBold.ttf")
Park_n_Go().run()


                
        

        