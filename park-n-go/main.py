import os
from jinja2 import Environment, FileSystemLoader
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
from datetime import timedelta
from server import start_serv
import threading
import time

# Loading .env file
load_dotenv()

# Initiating database credentials
USER = os.getenv('USER')
HOST = os.getenv('HOST')
DATABASE = os.getenv('DATABASE')
PASSWORD = os.getenv('PASSWORD')
PORT = os.getenv('PORT')

# Using Try-Catch to connect with database
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

        # Defining global vars
        self.userModel = ""
        self.entryTime = ""

        # Loading assets from Components
        self.screen = Builder.load_file("./Components/main.kv")
        
        # Defining items of dropdown box
        menu_items = [{"text": "Light Vehicle", "viewclass": "OneLineListItem", "on_release": lambda text="Light Vehicle": self.display_text(text)},
                      {"text": "Heavy Vehicle", "viewclass": "OneLineListItem",
                          "on_release": lambda text="Heavy Vehicle": self.display_text(text)},
                      {"text": "Bicycle", "viewclass": "OneLineListItem",
                          "on_release": lambda text="Bicycle": self.display_text(text)},
                      {"text": "Three wheeler", "viewclass": "OneLineListItem", "on_release": lambda text="Three Wheeler": self.display_text(text)}]
        
        # Creating the Dropdown box
        self.menu = MDDropdownMenu(
            caller=self.screen.get_screen('mainscreen').ids.drop,
            items=menu_items,
            width_mult=4,
        )

        return self.screen

    def get_info(self, user):
        # Fetching UserData from Database
        sql1 = "SELECT * from Net_Amount where Reg_no = %s"
        inputuser = (f"{user.text}",)
        mycursor.execute(sql1, inputuser)
        data = mycursor.fetchall()

        # Fetching Name & Phone Number from Database
        sql2 = "SELECT * from Parking where Reg_no = %s"
        inputuser = (f"{user.text}",)
        mycursor.execute(sql2, inputuser)
        data1 = mycursor.fetchall()
        return (data, data1)
    
    # Generating template 
    def details(self, data, data1):
        self.dialog.dismiss()
        print("Start generation")
        env = Environment( loader = FileSystemLoader("template/"))
        template = env.get_template('index.html')
        filename=f"template/generate_{data1[0][1]}.html"
        print(data, data1)

        # Writting data to the html template using jinja2
        write = {"name": data1[0][1], "phone": data1[0][2], "regNo": data[0][0],"entryTime": str(data[0][1]), "exitTime": str(data[0][2]), "car": data[0][3], "amount": str(data[0][4])}
        content = template.render(write)
        with open(file = f"{filename}", mode="w", encoding="utf-8") as ticket:
            ticket.write(content)

        # Creating a treaded object
        obj = start_serv(filename)

        stop_event = threading.Event()

        t1 = threading.Thread(target=obj.start_server, args=(stop_event,))
        t2 = threading.Thread(target=obj.open_file)

        # Starting both Threads
        t1.start()
        t2.start()

        time.sleep(1)

        # Stoping Threads
        stop_event.set()

        t1.join()
        t2.join()



    # A dialog box is  created to notify that login is not sucessfull
    def create_dialog(self, message):
        self.dialog = MDDialog(
                text=message,
                buttons=[
                    MDFlatButton(
                        text="Try Again",
                        on_release=lambda _: self.dialog.dismiss()
                    ),
                ],
            )
        self.dialog.open()

    # Another dialog box is created to notify that login is sucessfull
    def success_dialog(self, message, dismiss=True, data=True, data1=True):
        if dismiss:
            self.dialog = MDDialog(
                    text=message,
                    buttons=[
                        MDFlatButton(
                            text="Okay",
                            on_release=lambda _: self.dialog.dismiss()
                        ),
                    ],
                )
        else:
            self.dialog = MDDialog(
                    text=message,
                    buttons=[
                        MDFlatButton(
                            text="Okay",
                            on_release=lambda _: self.details(data, data1)
                        ),
                    ],
                )
        self.dialog.open()

    # Displaying text made under build function
    def display_text(self, text):
        print(text)
        self.menu.dismiss()
        self.userModel = text

    # Function to save following inputs in the database
    def save(self):

        # Getting input from MainScreen
        regNo = self.screen.get_screen('mainscreen').ids.regNo
        name = self.screen.get_screen('mainscreen').ids.name
        phno = self.screen.get_screen('mainscreen').ids.phno
        val = (regNo.text, name.text, phno.text, self.userModel, self.entryTime)
        print(self.entryTime)

        truth = not all(val)

        # Checking if all fields are filled
        if (not truth):
            
            # Fetching Name & Phone Number from Database
            fetchingQuery = "SELECT * from Parking where Reg_no = %s"
            inputuser = (f"{regNo.text}",)
            mycursor.execute(fetchingQuery, inputuser)
            fetchedData = mycursor.fetchone()

            if not fetchedData:
                sql = "INSERT INTO Parking (Reg_no, Name, Phone_no, Vehicle_mode, Entry_Time) VALUES (%s, %s, %s, %s, %s)"
                mycursor.execute(sql, val)
                mydb.commit()
                # A dialog box is created to notify user that data was saved to database
                self.success_dialog('Saved to Database')

            else:
                # A another dialog box is created to notify user that the  vehicle selected was already present in the database
                self.create_dialog('Vehicle is already present!')
        else:
            # A dialog box is created to notify user that Fields cannot be left empty
            self.create_dialog('Fields cannot be empty!')

    # Fetching details such as regno and data from database
    def DownloadReceipt(self):
        regno = self.screen.get_screen('billing').ids.text1
        data, data1 = self.get_info(regno)

        # Deleting from Net_Amount
        sql = "DELETE FROM Net_Amount where Reg_no = %s"
        inputuser = (f"{regno.text}",)
        mycursor.execute(sql, inputuser)
        mydb.commit()

        # Sending data to details() to generate the Receipt PDF
        self.success_dialog('MAKE SURE YOU DOWNLOAD THE PDF!', dismiss=False, data=data, data1=data1)

        # Deleting from Parking
        sql = "DELETE FROM Parking where Reg_no = %s"
        mycursor.execute(sql, inputuser)
        mydb.commit()

        # MySQL queries to remove vehicle from parking slot when receipt is downloaded
        print("Downloadeded Receipt", data, data1)
    
    # Rendering data to the app screen
    def showReceipt(self):
        user = self.screen.get_screen('billing').ids.text1

        if user.text == "":
            self.create_dialog("Enter the Registration number to Continue")
            
        else:

            data, data1 = self.get_info(user)

            # verifying if data is found in database
            if data == [] and data1 == []:
                self.create_dialog("Data not found in the database!")
            else:

                # Redirect to Receipt screen
                self.root.transition.direction = "left"
                self.root.current = "receipt"

                # Get ids from to Receipt Screen
                name = self.screen.get_screen('receipt').ids.name
                phone = self.screen.get_screen('receipt').ids.phone
                registration = self.screen.get_screen('receipt').ids.regNo
                check_in = self.screen.get_screen('receipt').ids.entryTime
                check_out = self.screen.get_screen('receipt').ids.exitTime
                car_mode = self.screen.get_screen('receipt').ids.car
                Amount = self.screen.get_screen('receipt').ids.amount

                # Render Data back to Receipt Screen
                name.text = data1[0][1]
                phone.text = data1[0][2]
                registration.text = data[0][0]
                check_in.text = str(data[0][1])
                check_out.text = str(data[0][2])
                car_mode.text = data[0][3]
                Amount.text = str(data[0][4])

                print("Served receipt data to Screen")

    def auth(self):

        # Fetching from Frontend
        user = self.screen.get_screen('login').ids.text1.text
        pwd = self.screen.get_screen('login').ids.passw.text

        # Fetch Admin Data from DB
        sql = "select * from admin"
        mycursor.execute(sql)
        res = mycursor.fetchall()
        userID = res[0][0]
        password = res[0][1]

        # Validation
        if pwd == password and int(user) == userID:
            self.root.transition.direction = "left"
            self.root.current = "register"
            print("Passed Authentication")
        else:
            self.create_dialog(message='Invalid username or password')

    def checkout(self):
        
        # Fetching Checkout Data Frontend
        regno = self.screen.get_screen('checkout').ids.regno
        print(regno.text, self.entryTime)
        if regno.text == "":
            self.create_dialog("Enter the Registration number to Continue")
        else:
            # Fetching Data
            sql = "select Reg_no from Parking"
            mycursor.execute(sql)
            records = mycursor.fetchall()
            records = [item for t in records for item in t]
            
            #Checking if the Vehicle is inside the parking area or not.
            if regno.text not in records:
                
                self.create_dialog('Vehicle not present inside the Parking slot')
            else:

                # Fetching Entry Time from Database
                sql = "SELECT Entry_Time from Parking where Reg_no = %s"
                inputuser = (f"{regno.text}",)
                mycursor.execute(sql, inputuser)
                time = mycursor.fetchall()
                entryTime_from_db = str(time[0][0])

                # Fetching Vehicle Model from Database
                sql = "SELECT Vehicle_mode from Parking where Reg_no = %s"
                inputuser = (f"{regno.text}",)
                mycursor.execute(sql, inputuser)
                model = mycursor.fetchall()
                model = str(model[0][0])

                if(len(entryTime_from_db)==7):
                    entryTime_from_db = '0'+entryTime_from_db

                # Calculating Total Time in hh:mm
                FetchedEntryTime = timedelta(hours=int(entryTime_from_db[:2]), minutes=int(entryTime_from_db[3:5]), seconds=int(entryTime_from_db[6:]))

                Checkout_time = timedelta(hours=int(self.entryTime[:2]), minutes=int(self.entryTime[3:5]), seconds=int(self.entryTime[6:]))

                # Calculating total Time spent in Parking Slot
                totalTime  = str(Checkout_time - FetchedEntryTime)
                
                # If Checked Out Next Day
                if totalTime[0] == '-':
                    totalTime = (totalTime.split("-1 day, "))[1]

                # Converting totalTime in terms of Hours 
                hours, minutes, seconds = map(int, totalTime.split(':'))
                total_hours = hours + minutes / 60 + seconds / 3600

                # Setting Tax as per Vehicle
                if model == 'Light Vehicle':
                    # 20 Rrupees per Hour
                    Amount = total_hours * 20.0
                elif model == 'Heavy Vehicle':
                    # 30 Rrupees per Hour
                    Amount = total_hours * 30.0
                elif model == 'Bicycle':
                    # 8 Rrupees per Hour
                    Amount = total_hours * 8.0
                elif model == 'Three Wheeler':
                    # 15 Rrupees per Hour
                    Amount = total_hours * 15.0
                else:
                    # By default it is light vehicle
                    Amount = total_hours * 20.0

                # MySQL queries to save checkout details
                sql = "INSERT INTO Net_Amount (Reg_no, Checkin_time, Checkout_time, Vehicle_mode, Amount) VALUES (%s, %s, %s, %s, %s)"
                val = (regno.text, str(FetchedEntryTime), str(Checkout_time),model, Amount)

                mycursor.execute(sql, val)
                mydb.commit()

                self.root.transition.direction="left"
                self.root.current="billing"
                print("Net_amount data saved to database")

    # Function to open time-picker
    def show_time_picker(self):
        '''Open time picker dialog.'''
        time_dialog = MDTimePicker()
        time_dialog.open()
        time_dialog.bind(on_save=self.get_time)

    # Function to get time and overwrite entryTime in __init__()
    def get_time(self, instance, time):
        time = time.strftime("%H:%M:%S")
        self.entryTime = time

# Driver Code
if __name__ == "__main__":
    LabelBase.register(
        name="MPoppins", fn_regular="assets/fonts/Poppins-Medium.ttf")
    LabelBase.register(
        name="BPoppins", fn_regular="assets/fonts/Poppins-SemiBold.ttf")
Park_n_Go().run()
