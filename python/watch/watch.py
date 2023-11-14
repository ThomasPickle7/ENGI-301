"""
--------------------------------------------------------------------------
People Counter
--------------------------------------------------------------------------
License:   
Copyright 2023 <Name>

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

import button as BUTTON
import smbus
import SSD1306
import AHT10
import MPU6050

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

class Watch():
    """ People Counter """
    reset_time = None
    button_set     = None
    button_toggle = None
    display    = None
    weather  = None
    gyro = None
    bus = None
    mode = None
    mil_time = False
    second_count = 0
    min_count = 0
    hour_count = 0
    meridian = True #True = AM, False = PM
    set_min = True #True = increment minutes, False =- increment hours
    def __init__(self, mil_time, reset_time=2.0, button_set="P2_2", button_toggle = "P2_4", i2c_bus = smbus.SMBus(1)):
        """ Initialize variables and set up display """
        self.reset_time = reset_time
        self.button_set     = BUTTON.Button(button_set)
        self.button_toggle = BUTTON.Button(button_toggle)
        self.display    = SSD1306.SSD1306(0x3c)
        self.gyro       = MPU6050.MPU6050(i2c_bus, 0x68)
        self.weather    = AHT10.AHT10(i2c_bus, 0x38)
        self.mode = True #True = toggle seconds, False = toggle hours
        self.mil_time = mil_time
        self._setup()
        if(mil_time): # Number of people to be displayed
            self.hour_count = 0
        else:
            self.hour_count = 12 # Number of people to be displayed
         #True=AM, False = PM
    
    # End def
    
    
    def _setup(self):
        """Setup the hardware components."""
        # Initialize Display
        
        self.display.blank()
        print("People Counter setup()")

    # End def

    def increment(self, wait):
        time.sleep(wait)
        self.second_count += 1
        if(self.second_count == 60):
            self.min_count += 1
            self.second_count = 0
            if(self.min_count == 60):
                self.hour_count += 1
                self.min_count = 0
                if(self.min_count == 60):
                    self.hour_count += 1
                if ((not self.mil_time) and (self.hour_count == 13 or self.hour_count == 25)):
                    self.hour_count = 1
                    self.meridian = not self.meridian
                if (self.mil_time and self.hour_count == 24):
                    self.hour_count = 0
                    self.meridian = not self.meridian
                     
        
    
    def toggle(self, wait):
        i=0
        period = 1 - wait
        while i  < (period * 10):
            i += 1
            button_press_toggle = self.button_toggle.is_pressed()
            
            button_press_set = self.button_set.is_pressed()
            
            if(button_press_toggle):
                self.set_min = not self.set_min

            if(button_press_set):
                if (self.set_min):
                    self.min_count += 1
                else:
                    self.hour_count += 1
                    
                if(self.min_count == 60):
                    self.hour_count += 1
                    self.min_count = 0
                if(self.hour_count == 60):
                    self.hour_count += 1
                if ((not self.mil_time) and (self.hour_count == 13 or self.hour_count == 25)):
                    self.hour_count = 1
                if (self.hour_count % 12 == 0):
                    self.meridian = not self.meridian  
                if (self.mil_time and self.hour_count == 24):
                    self.hour_count = 0
                        
                time.sleep(((period * 10) - i) * .1)
                break
            time.sleep(wait)
            
            
            
        
    def display_time(self):
        """Increments the clock."""
            
            # Update the display
        if(self.meridian):
            meri_text = " AM"
        else:
            meri_text = " PM"
        if(self.second_count < 10):
            second_text = "0" + str(self.second_count)
        else:
            second_text = str(self.second_count)
        
        if(self.min_count < 10):
            min_text = "0" + str(self.min_count)
        else:
            min_text = str(self.min_count)
            
        if(self.hour_count < 10):
            hour_text = "0" + str(self.hour_count)
        else:
            hour_text = str(self.hour_count)
                
        text = hour_text + ":" + min_text + ":" + second_text + meri_text
        return text

    # End def
    def cleanup(self):
        """Setup the hardware components."""
        # Initialize Display
        
        self.display.update_text("DEAD!")
# End class



# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':

    print("Program Start")

    # Create instantiation of the people counter
    watch = Watch(False)
    display = SSD1306.SSD1306(0x3c)
    freq = 10
    period = 1/freq
    try:
        # Run the people counter
        while (True):
            watch.increment(period)
            watch.toggle(period)
            text = watch.display_time()
            print(text)
            display.update_text(text)
            

    except KeyboardInterrupt:
        # Clean up hardware when exiting
        watch.run(True)

    print("Program Complete")

