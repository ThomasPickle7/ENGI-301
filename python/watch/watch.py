"""
--------------------------------------------------------------------------
Watch
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
Software API:

  Watch(bus, address=0x70)
    - Provide i2c bus that dispaly is on
    - Provide i2c address for the display
    
    increment()
      - Sets value of display to "0000"
    
    toggle()
      - Turns off all LEDs on display
    
    time(enable)
      - Turns on / off the colon on the display.  Enable must be True/False.
    
    display_time(value)
      - Update the value on the display.  Value must be between 0 and 9999.

    text(value)
      - Update the value on the display with text.
        The following characters are supported:
            "abcdefghijlnopqrstuyABCDEFGHIJLNOPQRSTUY? -"
  
--------------------------------------------------------------------------

"""
import time
import multiprocessing
import Adafruit_BBIO.GPIO as GPIO

import button as BUTTON
import smbus
import SSD1306

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
    button_set     = None
    button_toggle = None
    mil_time = False
    second_count = 0
    min_count = 0
    hour_count = 0
    meridian = True #True = AM, False = PM
    set_min = True #True = increment minutes, False = increment hours
    def __init__(self, mil_time, button_set="P2_2", button_toggle = "P2_4", i2c_bus = smbus.SMBus(1)):
        """ Initialize variables and set up display """
        self.button_set     = BUTTON.Button(button_set)
        self.button_toggle = BUTTON.Button(button_toggle)
        self.mil_time = mil_time
        if(mil_time): # Changes the clock's interpretation of midnight/noon based on preferred configuration
            self.hour_count = 0
        else:
            self.hour_count = 12
         
    
    # End def
    

    # End def

    def increment(self):
        """Synchronously updates the time"""
        while True:
            self.second_count += 1
            return self.second_count

                     
        
    
    def toggle(self):
        """Allows the user to toggle the hours and minutes on the clock based on the state of the toggle bbutton"""
        
        while True:
            button_press_toggle = self.button_toggle.is_pressed()
            
            button_press_set = self.button_set.is_pressed()
            
            if(button_press_toggle):
                self.set_min = not self.set_min

            if(button_press_set):
                if (self.set_min):
                    self.min_count += 1
                else:
                    self.hour_count += 1
            return (self.min_count, self.hour_count)
            
            
    def time(self):
        while True:
          #Allows the incremented and toggled time to be added in parallel
            seconds = self.increment()
            (mins, hrs) = self.toggle()
            if(seconds >= 60):
                self.min_count += 1
                self.second_count = 0
            if(mins >= 60):
                self.hour_count += 1
                self.min_count = 0
                if ((not self.mil_time) and (self.hour_count == 12 or self.hour_count == 24)):
                    self.hour_count = 1
                    self.meridian = not self.meridian
                if (self.mil_time and self.hour_count == 23):
                    self.hour_count = 0
                   
            return (hrs, mins, seconds)
            
        
    def display_time(self):
        """Returns a string version of the current time."""
            
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


# End class



# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':

    print("Program Start")

    # Create instantiation of the watch and display
    watch = Watch(False)
    display = SSD1306.SSD1306(0x3c)
    
    try:
        # Run the people counter
        while (True):
            timing = watch.time()
            disp_text = watch.display_time()
            display.update_text(disp_text)
            print(disp_text)
            time.sleep(1)
            

    except KeyboardInterrupt:
        # Clean up hardware when exiting
        watch.run(True)

    print("Program Complete")

