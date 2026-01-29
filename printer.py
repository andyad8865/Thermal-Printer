import sys
import io
import time
import os
import textwrap
from Adafruit_Thermal import *

# 1. Initialize Hardware (9V / 9600 Baud / FW 2.67)
printer = Adafruit_Thermal("/dev/serial0", 9600, timeout=5)
printer.firmwareVersion = 267
printer.begin(100) # HeatTime 100 via begin() for 9V

def run_thermal_job(input_data, raw_mods_string):
    printer.wake()
    printer.reset() 
    mods = [m.strip().lower() for m in raw_mods_string.split(",")]

    # --- BRANCH 1: DIAGNOSTICS ---
    if "test" in mods:
        printer.writeBytes(18, 84) # DC2 T (Hard Test)
        time.sleep(5.0)
        os._exit(0)
        
    elif "test_all" in mods:
        # (Retail barcode test suite)
        test_suite = [("UPC-A",65,"075678164125"),("UPC-E",66,"01234500005"),("EAN13",67,"4006381333931"),("CODE39",69,"ABC-123"),("C128",73,"V128")]
        for name, bc_id, data in test_suite:
            printer.setSize('S')
            printer.println(f"TYPE: {name}")
            printer.writeBytes(29, 72, 2)
            printer.writeBytes(29, 107, bc_id)
            printer.writeBytes(len(data))
            for char in data: printer.writeBytes(ord(char))
            printer.feed(2); time.sleep(1.5)
        os._exit(0)

    # --- BRANCH 2: IMAGES ---
    elif "img" in mods:
        try:
            from PIL import Image
            import requests
            printer.writeBytes(27, 55, 11, 185, 250)
            printer.writeBytes(27, 51, 100) # Max spacing for image
            if input_data.startswith('http'):
                res = requests.get(input_data, timeout=10)
                img_obj = Image.open(io.BytesIO(res.content))
            else:
                img_obj = Image.open(input_data)
            
            scale = 100
            for m in mods:
                if m.startswith('s') and m[1:].isdigit(): scale = int(m[1:])
            
            tw = max(8, min(384, (int(384 * (scale / 100.0)) // 8) * 8))
            img_obj = img_obj.resize((tw, int(img_obj.height * (tw/img_obj.width))), Image.Resampling.NEAREST).convert('1')
            printer.printImage(img_obj, False)
            printer.feed(2); time.sleep(3)
        finally:
            os._exit(0)

    # --- BRANCH 3: BARCODES ---
    elif any(x in mods for x in ["upca","upce","ean13","ean8","code39","itf","cobar","code93","c128"]):
        printer.writeBytes(27, 51, 30) # Reset spacing
        bc_map = {"upca":65,"upce":66,"ean13":67,"ean8":68,"code39":69,"itf":70,"cobar":71,"code93":72,"c128":73}
        bc_type = 69
        for mod in mods:
            if mod in bc_map: bc_type = bc_map[mod]
            if mod.startswith('h') and mod[1:].isdigit(): printer.writeBytes(29, 104, int(mod[1:]))
            if mod.startswith('w') and mod[1:].isdigit(): printer.writeBytes(29, 119, int(mod[1:]))
        
        data = input_data.upper() if "code39" in mods else input_data
        printer.writeBytes(29, 72, 2)
        printer.writeBytes(29, 107, bc_type)
        printer.writeBytes(len(data))
        for char in data: printer.writeBytes(ord(char))
        printer.writeBytes(27, 74, 60); time.sleep(1.5)
        os._exit(0)

    # --- BRANCH 4: THE COMPLETE TEXT WRAPPER ---
    else:
        # 1. CHARACTER LIMITS (Word Wrap)
        char_limit = 32
        if "large" in mods: 
            char_limit = 16
            printer.setSize('L')
        elif "med" in mods: 
            char_limit = 21
            printer.setSize('M')
        else: 
            printer.setSize('S')

        # 2. FORMATTING FUNCTIONS SUPPORTED BY LIB
        if "b" in mods: printer.boldOn()               # printer.boldOn()
        if "inv" in mods: printer.inverseOn()          # printer.inverseOn()
        if "up" in mods: printer.upsideDownOn()        # printer.upsideDownOn()
        if "dh" in mods: printer.doubleHeightOn()      # printer.doubleHeightOn()
        if "dw" in mods: printer.doubleWidthOn()        # printer.doubleWidthOn()
        
        # Underlines
        if "ult" in mods: printer.underlineOn(2)       # printer.underlineOn(2)
        elif "ul" in mods: printer.underlineOn(1)       # printer.underlineOn(1)
        
        # Justification
        if "jc" in mods: printer.justify('C')          # printer.justify('C')
        elif "jr" in mods: printer.justify('R')        # printer.justify('R')
        else: printer.justify('L')                     # printer.justify('L')

        # 3. PRINT WRAPPED LINES
        wrapped = textwrap.wrap(input_data, width=char_limit)
        for line in wrapped:
            printer.println(line)

        # 4. DYNAMIC FEED
        for m in mods:
            if m.startswith('f') and m[1:].isdigit():
                num = int(m[1:])
                printer.feed(num)
                time.sleep(num * 0.2)
                break 

        printer.reset()
        printer.sleep()
        os._exit(0)

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        run_thermal_job(sys.argv[1], sys.argv[2])
