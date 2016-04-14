#!/usr/bin/python
import serial
import signal
import sys
import os

import time
import serial
from Tkinter import *

#ser = serial.Serial('COM5', 115200, timeout=0)
#print ser.portstr

# Serial port parameters
serial_speed = 115200
serial_port = 'COM5'

ser = serial.Serial(serial_port, serial_speed, timeout=1)
h2 = ('Verdana', 20, 'bold')

human_texts = ['HV AMPS', 'HV VOLT', 'LV AMPS', 'LV VOLT', \
              'TEMP 1', 'TEMP 2', 'TEMP 3', 'TEMP 4', \
              'MOD 1', 'MOD 2', 'MOD 3', 'MOD 4']

serial_texts = ['I_HV', 'V_HV', 'I_LV', 'V_LV', \
               'T1', 'T2', 'T3', 'T4', \
               'MOD1', 'MOD2', 'MOD3', 'MOD4']

human_readable_dict = dict(zip(serial_texts, human_texts))



# Main Tkinter application
class Application(Frame):

    # Measure data from the sensor
    def measure(self):
        #print 'measuring'

        # read data 
        data = ser.readline()
        title = ''

        # If the answer is not empty, process & display data
        if (data != ""):
            data = data.split(",")
            case = data[0]
            data = data[1:]
            #print 'data', data
            
            #if case == 'A' and len(data) == 2*len(human_readable_dict):
            if case == 'A':
                vals_dict = dict(u.split(":") for u in data)
                for serial_key, val in vals_dict.items():
                    human_text = human_readable_dict[serial_key]
                    title = human_text + ': ' + str(val)
                    #print self.tk_vars_dict
                    var = self.tk_vars_dict[serial_key]
                    var.set(title)

                #update_vals(key)            
                #elif case == 'B':
                #self.after(100,self.measure)

            

            #else:
                #TODO: Throw an error
                    
            # Wait 1 second between each measurement
        self.after(100,self.measure)

    # Create display elements
    def createWidgets(self):
        #self.LIM1= Label(textvariable=self.lim1_data, font=h2).grid(row=0, column=0)
        #self.LIM2= Label(textvariable=self.lim2_data, font=h2).grid(row=1, column=0)
        #self.AMC = Label(textvariable=self.amc_data, font=h2).grid(row=2, column=0)
        #self.BOOST1 = Label(textvariable=self.boost1_data, font=h2).grid(row=0, column=1)
        #self.BOOST2 = Label(textvariable=self.boost2_data, font=h2).grid(row=0, column=2)
        #self.columnconfigure(0,pad = 2)
        #self.columnconfigure(1,pad = 2)
        self.hv_amps, self.hv_volts, self.lv_amps, self.lv_volts, \
                          self.temp1, self.temp2, self.temp3, self.temp4, \
                          self.mod1, self.mod2, self.mod3, self.mod4 \
                          = [StringVar() for _ in range(12)]
            
        self.tk_vars = [self.hv_amps, self.hv_volts, self.lv_amps, self.lv_volts, \
                          self.temp1, self.temp2, self.temp3, self.temp4, \
                          self.mod1, self.mod2, self.mod3, self.mod4]
        
        i = 0
        self.tk_vars_dict = {}
        
        for tk_var, serial_text in zip(self.tk_vars, serial_texts):
            tk_var.set('nyan')
            lb = Label(textvariable = tk_var, font=h2)
            lb.grid(row=i, column=1)
            self.tk_vars_dict[serial_text] = tk_var
            i += 1
        
    # Init the variables & start measurements
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.createWidgets()
        self.measure()


#def on_closing():
#    print('Closing serial port!')
#    ser.close()
#    root.destroy()


def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    ser.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Create and run the GUI
root = Tk()
#root.protocol("WM_DELETE_WINDOW", on_closing)
app = Application(master=root)
app.mainloop()

ser.close()
print "Closed serial port!"

