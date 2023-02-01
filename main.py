import PySimpleGUI as sg
import datetime as dt

sg.theme('DarkBlack')   
# Add a touch of color

#Car models
Models = ['Honda', 'Toyota', 'Chevrolet', 'Jeep', 'Ford', 'Bolero', 'SUV', 'SwiftDesire', 'Sedan']

# All the stuff inside your window.
layout = [  
            [sg.Text('Welcome to Park-n-Go')],
            [sg.Text('A tool to track and Save Details of Vehicles Entering the Parking Zone')],
            [sg.Text('Enter Registration Number : '), sg.InputText()],
            [sg.Text('Choose Model : '), sg.Combo(Models)],
            [sg.Text('Parking Space ID : '), sg.InputText()],
            [sg.Text('Time of Entry : '), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Cancel')] 
        ]

# Create the Window
window = sg.Window('Park-n-Go', layout, font='Helvetica 12', element_justification='c')
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    print(values)

window.close()