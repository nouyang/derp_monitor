#!/usr/bin/python
import serial
import signal
import sys
import os

import time
import serial
from Tkinter import *


# Serial port parameters
serial_speed = 115200
serial_port = 'COM5'

ser = serial.Serial(serial_port, serial_speed, timeout=1)
ser.close()
ser.open()

h2 = ('Verdana', 20, 'bold')
title = 'OrangeNarwhals Telemetry'


bgcolorA = 'orange'
bgcolorB = 'purple' #hex works too, e.g. '#FFFFFF'

human_texts = ['HV AMPS', 'HV VOLT', 'LV AMPS', 'LV VOLT', \
              'TEMP 1', 'TEMP 2', 'TEMP 3', 'TEMP 4', \
              'MOD 1', 'MOD 2', 'MOD 3', 'MOD 4']

serial_texts = ['I_HV', 'V_HV', 'I_LV', 'V_LV', \
               'T1', 'T2', 'T3', 'T4', \
               'MOD1', 'MOD2', 'MOD3', 'MOD4']

row_cols = ['00', '01', '10', '11', \
            '20', '30', '21', '31', \
            '02', '12', '22', '32']

human_readable_dict = dict(zip(serial_texts, human_texts))
label_locations_dict = dict(zip(serial_texts, row_cols))

# Main Tkinter application
class Application(Frame):

    def measure(self):
        # read data
        data = ser.readline().strip()
        title = ''

        # If the answer is not empty, process & display data
        if (data != ""):
            data = data.split(",")
            case = data[0]
            data = data[1:]
            #print 'data', data
            
            #if case == 'A' and len(data) == 2*len(human_readable_dict):
            if case == 'A' or case == 'B':
                vals_dict = dict(u.split(":") for u in data)
                for serial_key, val in vals_dict.items():
                    human_text = human_readable_dict[serial_key]
                    title = human_text + ': ' + str(val)
                    #print self.tk_vars_dict
                    if case == 'A':
                        var = self.tk_vars_dict[serial_key]
                    else:
                        var = self.B_tk_vars_dict[serial_key]
                    var.set(title)
                    
            #else:
                #TODO: Throw an error
                    
            # Wait 1 second between each measurement
        self.after(100,self.measure)

    # Create display elements
    def createWidgets(self):
        #self.LIM1= Label(textvariable=self.lim1_data, font=h2).grid(row=0, column=0)

        self.hv_amps, self.hv_volts, self.lv_amps, self.lv_volts, \
                          self.temp1, self.temp2, self.temp3, self.temp4, \
                          self.mod1, self.mod2, self.mod3, self.mod4 \
                          = [StringVar() for _ in range(12)]
            
        self.tk_vars = [self.hv_amps, self.hv_volts, self.lv_amps, self.lv_volts, \
                          self.temp1, self.temp2, self.temp3, self.temp4, \
                          self.mod1, self.mod2, self.mod3, self.mod4]

        self.B_hv_amps, self.B_hv_volts, self.B_lv_amps, self.B_lv_volts, \
                          self.B_temp1, self.B_temp2, self.B_temp3, self.B_temp4, \
                          self.B_mod1, self.B_mod2, self.B_mod3, self.B_mod4 \
                          = [StringVar() for _ in range(12)]
            
        self.B_tk_vars = [self.B_hv_amps, self.B_hv_volts, self.B_lv_amps, self.B_lv_volts, \
                          self.B_temp1, self.B_temp2, self.B_temp3, self.B_temp4, \
                          self.B_mod1, self.B_mod2, self.B_mod3, self.B_mod4]
        
        i = 0
        self.tk_vars_dict = {}
        self.B_tk_vars_dict = {}
        
        for tk_var, serial_text in zip(self.tk_vars, serial_texts):
            tk_var.set('nyannnnnnnnn')
            lb = Label(self.FrameA, textvariable = tk_var, font = h2, bg = bgcolorA)
            row, col = label_locations_dict[serial_text]
            lb.grid(row = row, column = col, sticky = 'W', padx = 15, pady = 2)
            self.tk_vars_dict[serial_text] = tk_var
            i += 1
            
        for B_tk_var, serial_text in zip(self.B_tk_vars, serial_texts):
            B_tk_var.set('nyannnnnnnnnn')
            lb = Label(self.FrameB, textvariable = B_tk_var, font = h2, bg = bgcolorB)
            row, col = label_locations_dict[serial_text]
            lb.grid(row = row, column = col, sticky = 'W', padx = 15, pady = 2)
            self.B_tk_vars_dict[serial_text] = B_tk_var
            i += 1
        
    # Init the variables & start measurements
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.master.title("OrangeNarwhals Telemetry")

        self.FrameA = Frame(master, bg = bgcolorA)
        self.FrameB = Frame(master, bg = bgcolorB)

        self.FrameA.grid(row = 0, column = 0, rowspan = 4, columnspan = 3, sticky = 'W')
        self.FrameB.grid(row = 5, column = 0, rowspan = 4, columnspan = 3, sticky = 'W')
        
        for r in range(5):
             self.FrameA.rowconfigure(r, weight = 1)
             self.FrameB.rowconfigure(r, weight = 1)
             root.grid_rowconfigure(r, weight=1)
        for c in range(3):
             self.FrameA.columnconfigure(c, weight = 1)
             self.FrameB.columnconfigure(c, weight = 1)
             root.grid_columnconfigure(c, weight=1)
        
        self.createWidgets()
        root.update()
        root.minsize(root.winfo_width(), root.winfo_height())
        root.configure(background = bgcolorA)
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

