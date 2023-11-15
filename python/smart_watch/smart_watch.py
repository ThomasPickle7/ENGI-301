"""
--------------------------------------------------------------------------
Smart Watch
--------------------------------------------------------------------------
License:   
Copyright 2023 Thomas Pickell

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Use the HT16K33 Display and a button to create a digital people counter

Requirements:
  - Increment the counter by one each time the button is pressed
  - If button is held for more than 2s, reset the counter

Uses:
  - HT16K33 display library developed in class

"""
import time
import multiprocessing
import Adafruit_BBIO.GPIO as GPIO

import smbus
import SSD1306
import AHT10
import MPU6050
import button as BUTTON
import watch as WATCH
import pedometer as PED

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

# None

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

# None

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class SmartWatch():
    """ People Counter """
    ped = None
    watch = None
    time = None
    toggle_button = None
    display = None
    time_screen = True #True= show time, False = show fitness data
    def __init__(self, button_address = "P2_6", i2c_bus = smbus.SMBus(1)):
        """ Initialize variables and set up display """
        self.toggle_button = BUTTON.Button("P2_6")
        self.ped = PED.Pedometer(False)
        self.watch = WATCH.Watch(False)
        self.display = SSD1306.SSD1306(0x3c)
        
        
         
    
    # End def

    # End def

    def get_data(self):
        """Synchronously updates the time"""
        while True:
            return self.ped.get_data()
        
    def get_time(self):
        while True:
            self.watch.time()
            return self.watch.display_time()
    def choose(self):
        while True:
            button_pressed = self.toggle_button.is_pressed()
            time = self.get_time()
            data = self.get_data()
            if(button_pressed):
                self.time_screen = not self.time_screen
            if self.time_screen:
                return time
            else:
            
                return data
# End class



# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':

    print("Program Start")

    # Create instantiation of the watch and display
    swatch = SmartWatch(False)
    display = SSD1306.SSD1306(0x3c)
    try:
        # Run the people counter
        while (True):

            disp = swatch.choose()
            print(disp)
            display.update_text(disp)
            time.sleep(1)

    except KeyboardInterrupt:
        # Clean up hardware when exiting
            display.blank()
    print("Program Complete")

