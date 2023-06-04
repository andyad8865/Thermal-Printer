#!/usr/bin/python

import sys
from Adafruit_Thermal import *

printer = Adafruit_Thermal("/dev/serial0", 9600, timeout=5)

printer.setDefault()

def has_paper():
    # Check if the printer has paper.  This only works if the RX line is connected
    # on your board (but BE CAREFUL as mentioned above this RX line is 5V!)
    if printer.hasPaper():
        print("Printer has paper!")
    else:
        print("Printer might be out of paper, or RX is disconnected!")

def print_bold(x):
    printer.wake()
    printer.boldOn()
    printer.println(x)
    printer.boldOff()

def print_underline(x):
    printer.wake()
    printer.underlineOn()
    printer.println(x)
    printer.underlineOff()

def print_underline_thick(x):
    printer.wake()
    printer.underlineOn(2)
    printer.println(x)
    printer.underlineOff()

def print_inverted(x):
    printer.wake()
    printer.inverseOn()
    printer.println(x)
    printer.inverseOff()

def print_double_height(x):
    printer.wake()
    printer.doubleHeightOn()
    printer.println(x)
    printer.doubleHeightOff()

def print_double_width(x):
    printer.wake()
    printer.doubleWidthOn()
    printer.println(x)
    printer.doubleWidthOff()

def print_medium(x):
    printer.wake()
    printer.setSize('M')
    printer.println(x)
    printer.setSize('S')

def print_large(x):
    printer.wake()
    printer.setSize('L')
    printer.println(x)
    printer.setSize('S')


def options (option, info):
    option = int(option)
    #Paper Check
    if option == 1:
        has_paper()
    
    #Paper Feed
    elif option == 2:
        if info == "":
            print ("No Number Detected, Please use a whole number between 1 and 255, Please use this format: printer.py 2 'Your Text Here'")
        else:
            try:
                printer.feed(int(info))
            except ValueError:
                print("No valid Number Detected, Please use a whole humber between 1 and 255")
    
    #Print Standard            
    elif option == 3:
        if info == "":
            print ("No Information Detected, Please use this format: printer.py 3 'Your Text Here'")
        else:
            printer.wake()
            printer.println(info)
    
    #Print Bold        
    elif option == 4:
        if info == "":
            print ("No Information Detected, Please use this format: printer.py 4 'Your Text Here'")
        else:
            print_bold(info)
    
    #Print Underline     
    elif option == 5:
        if info == "":
            print ("No Information Detected, Please use this format: printer.py 5 'Your Text Here'")
        else:
            print_underline(info)
    
    #Print Thick Underline        
    elif option == 6:
        if info == "":
            print ("No Information Detected, Please use this format: printer.py 6 'Your Text Here'")
        else:
            print_underline_thick(info)
    
    #Print Inverted (White Text On Black Background)
    elif option == 7:
        if info == "":
            print ("No Information Detected, Please use this format: printer.py 7 'Your Text Here'")
        else:
            print_inverted(info)
            
    #Print Double Height        
    elif option == 8:
        if info == "":
            print ("No Information Detected, Please use this format: printer.py 8 'Your Text Here'")
        else:
            print_double_height(info)
    
    #Print Double Width
    elif option == 9:
        if info == "":
            print ("No Information Detected, Please use this format: printer.py 9 'Your Text Here'")
        else:
            print_double_width(info)
    
    #Print Help Message On Console
    elif option == 'h' or 'help':
        print ("Welcome To The Help Page, Below Is A List Of All The Supported Commands")
        print ("#######################################################################")
        
    else:
        print("Invalid Option - Please Select a Number Between 1 and 9 OR Pass 'h' or 'help' for all commands")

########################################################
################## Script Starts Here ##################
########################################################
printer.setDefault()

try:
    option1 = sys.argv[1]
except ValueError: 
    print("No valid Number Detected, Please Select a Number Between 1 and 9") 
    quit()

if len(sys.argv[1:]) < 2:
    option2 = ""
else:
    option2 = sys.argv[2]
    
options(option1, option2)

#options(7, "Hello World!")
#options(2, 1)

if sys.argv[1] == '1':
  print("")
else:
  printer.feed(0)


printer.sleep()
