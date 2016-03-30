#!/usr/bin/python
import serial
import signal
import sys
import os

import time
import serial
from Tkinter import *

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
print ser.portstr

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    ser.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

#while True:
#    print ser.readline()


# Graphical User Interface for the Bluetooth sensor

# Serial port parameters
serial_speed = 9600
serial_port = '/dev/ttyUSB0'

# Test with USB-Serial connection
# serial_port = '/dev/tty.usbmodem1421'

ser = serial.Serial(serial_port, serial_speed, timeout=1)
h2 = ('Verdana', 20, 'bold')

LIM_text = ['HV AMPS', 'HV VOLT', 'LV AMPS', 'LV VOLT']
AMC_text = ['FAULT 1', 'FAULT 2', 'VOLT 1', 'VOLT 2', 'AMPS 1', 'AMPS 2']
BOOST_text = ['T1', 'T2', 'T3', 'T4', 'V1', 'V2', 'V3', 'V4']

keys = {'L1HVA':['LIM 1', LIM_text], \
        'L2HVA':['LIM 2', LIM_text], \
        'B1T1': ['BOOST 1', BOOST_text], \
        'B2T1': ['BOOST 2', BOOST_text], \
        'A1F1': ['AMC', AMC_text] \
        }

# Main Tkinter application
class Application(Frame):

    # Measure data from the sensor
    def measure(self):

        # read data 
        data = ser.readline()
        label = ''
        title = ''

        # If the answer is not empty, process & display data
        if (data != ""):
            data = data.split(",")
            case = data[0]
            
            if case in keys:
                title = keys[case][0]
                label = keys[case][1]
            else:
                self.after(100,self.measure)

            num = data[1::2] #strip out the labels

            if len(num) == len(label): #expected number of values
                foo = zip(label, num) #add in human-friendly labels 
                text = "\n".join("%s: %s" % tup for tup in foo)

                printout = title + '\n' + text
                if case == 'L1HVA':
                    self.lim1_data.set(printout)
                elif case == 'L2HVA':
                    self.lim2_data.set(printout)
                elif case == 'B1T1':
                    self.boost1_data.set(printout)
                elif case == 'B2T1':
                    self.boost2_data.set(printout)
                elif case == 'A1F1':
                    self.amc_data.set(printout)


            # Wait 1 second between each measurement
            self.after(100,self.measure)

    # Create display elements
    def createWidgets(self):
        self.LIM1= Label(textvariable=self.lim1_data, font=h2).grid(row=0, column=0)
        self.LIM2= Label(textvariable=self.lim2_data, font=h2).grid(row=1, column=0)
        self.AMC = Label(textvariable=self.amc_data, font=h2).grid(row=2, column=0)
        self.BOOST1 = Label(textvariable=self.boost1_data, font=h2).grid(row=0, column=1)
        self.BOOST2 = Label(textvariable=self.boost2_data, font=h2).grid(row=0, column=2)
        self.columnconfigure(0,pad = 2)
        self.columnconfigure(1,pad = 2)
        
    # Init the variables & start measurements
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.lim1_data = StringVar()
        self.lim2_data = StringVar()
        self.amc_data = StringVar()
        self.boost1_data = StringVar()
        self.boost2_data = StringVar()
        self.createWidgets()
        self.measure()

# Create and run the GUI
root = Tk()
app = Application(master=root)
app.mainloop()

