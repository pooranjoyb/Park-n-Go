import os
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivymd.uix.pickers import MDTimePicker
from kivymd.uix.menu import MDDropdownMenu
import mysql.connector as ms
from dotenv import load_dotenv
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

load_dotenv()
USER = os.getenv('USER')
HOST = os.getenv('HOST')
DATABASE = os.getenv('DATABASE')
PASSWORD = os.getenv('PASSWORD')
PORT = os.getenv('PORT')

try:
    mydb = ms.connect(host=HOST, user=USER, database=DATABASE,
                      password=PASSWORD, port=PORT)
    print("Connected to database")
    mycursor = mydb.cursor()
except:
    print("Cannot connect to database")


# Set pre defined window size
Window.size = (600, 600)


class WindowManager(ScreenManager):
    pass


class Park_n_Go(MDApp):
    def build(self):

        self.userModel = ""
        self.entryTime = ""

        self.screen = Builder.load_file("./Components/main.kv")
        menu_items = [{"text": "Light Vehicle", "viewclass": "OneLineListItem", "on_release": lambda text="Light Vehicle": self.display_text(text)},
                      {"text": "Heavy Vehicle", "viewclass": "OneLineListItem",
                          "on_release": lambda text="Heavy Vehicle": self.display_text(text)},
                      {"text": "Bicycle", "viewclass": "OneLineListItem",
                          "on_release": lambda text="Cycle": self.display_text(text)},
                      {"text": "Three wheeler", "viewclass": "OneLineListItem", "on_release": lambda text="3-Wheeler": self.display_text(text)}]
        self.menu = MDDropdownMenu(
            caller=self.screen.get_screen('mainscreen').ids.drop,
            items=menu_items,
            width_mult=4,
        )
        return self.screen

    def display_text(self, text):
        self.menu.dismiss()
        self.userModel = text

    def save(self):

        # Getting input from MainScreen
        regNo = self.screen.get_screen('mainscreen').ids.regNo
        name = self.screen.get_screen('mainscreen').ids.name
        phno = self.screen.get_screen('mainscreen').ids.phno

        # MySQL queries to save data
        sql = "INSERT INTO Parking (Reg_no, Name, Phone_no, Vehicle_mode, Entry_Time) VALUES (%s, %s, %s, %s, %s)"
        val = (regNo.text, name.text, phno.text, self.userModel, self.entryTime)

        mycursor.execute(sql, val)
        mydb.commit()

        # print(regNo.text, name.text, phno.text, self.userModel, self.entryTime)

        print("Saved to Database")

    def DownloadReceipt(self):
        print("Downloadeded Receipt")

    def showReceipt(self):
        print("Served receipt data to Screen")

    def auth(self):

        # Fetching from Frontend
        user = self.screen.get_screen('login').ids.text1.text
        pwd = self.screen.get_screen('login').ids.passw.text
        print(user, pwd)

        # Fetch Admin Data from DB
        sql = "select * from admin"
        mycursor.execute(sql)
        res = mycursor.fetchall()
        userID = res[0][0]
        password = res[0][1]
        print(userID)
        print(password)
 
        # Validation
        if pwd == password and int(user) == userID:
            self.root.transition.direction="left"
            self.root.current="register"
            print("Passed Authentication")
        else:
            print("INVALID PASSWORD")
            
    #     self.dialog = MDDialog(
    #     text="Invalid Username or Pass",
    #     buttons=[
    #         MDFlatButton(
    #             text="Try Again",
    #             on_release=lambda _: self.dialog.dismiss()
    #         ),
    #         MDFlatButton(
    #             text="EXIT",
    #             on_release=print("Hello World")
    #         ),
    #     ],
    # )
    #     self.dialog.open()

    def show_time_picker(self):
        '''Open time picker dialog.'''
        time_dialog = MDTimePicker()
        time_dialog.open()
        time_dialog.bind(on_save=self.get_time)

    def saveTodb(self):
        print("Data saved to database")

    def get_time(self, instance, time):
        time = time.strftime("%H:%M:%S")
        self.entryTime = time

if __name__ == "__main__":
    LabelBase.register(
        name="MPoppins", fn_regular="assets/fonts/Poppins-Medium.ttf")
    LabelBase.register(
        name="BPoppins", fn_regular="assets/fonts/Poppins-SemiBold.ttf")
Park_n_Go().run()
