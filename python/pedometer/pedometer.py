"""
--------------------------------------------------------------------------
Pedometer
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

class Pedometer():
    """ People Counter """
    display    = None
    gyro = None
    temp = None
    weather = None
    steps = None
    degree = False #False = Temp in Celsius, True = Temp in Farenheit
    def __init__(self, degree, i2c_bus = smbus.SMBus(1)):
        """ Initialize variables and set up display """
        self.temp     = AHT10.AHT10(i2c_bus, 0x38)
        self.gyro = MPU6050.MPU6050(i2c_bus, 0x68)
        self.degree = degree
        
         
    
    # End def

    # End def

    def get_data(self):
        """Synchronously updates the time"""
        while True:
            self.steps = self.gyro.run()
            self.weather = self.temp.run(self.degree)
            return str(self.steps)+", "+self.weather
        
        
            
            
            
        
# End class



# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':

    print("Program Start")

    # Create instantiation of the watch and display
    ped = Pedometer(False)
    display = SSD1306.SSD1306(0x3c)
    
    try:
        # Run the people counter
        while (True):

            text = ped.get_data()
            print(text)
            display.update_text(text)
            time.sleep(.3)

    except KeyboardInterrupt:
        # Clean up hardware when exiting
            display.blank()
    print("Program Complete")

