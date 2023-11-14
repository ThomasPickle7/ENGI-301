"""
--------------------------------------------------------------------------
AHT10 SMBUS Library
--------------------------------------------------------------------------
License:   
Copyright 2018-2023 <NAME>

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

  PU6050(bus, address=0x68)
    - Provide i2c bus that dispaly is on
    - Provide i2c address for the display
    
    clear()
      - Sets value of display to "0000"
    
    blank()
      - Turns off all LEDs on display
    
    set_colon(enable)
      - Turns on / off the colon on the display.  Enable must be True/False.
    
    update(value)
      - Update the value on the display.  Value must be between 0 and 9999.

    text(value)
      - Update the value on the display with text.
        The following characters are supported:
            "abcdefghijlnopqrstuyABCDEFGHIJLNOPQRSTUY? -"
  
--------------------------------------------------------------------------
Background Information: 
 
  
"""
import smbus	#import SMBus module of I2C
import math
from time import sleep 


class AHT10:
    def __init__(self, bus, address=0x38):
        """ Initialize class variables; Set up display; Set display to blank """
        
        # Initialize class variable=
        print("AHT10:")
        print("    Bus     = {0}".format(bus))
        print("    Address = 0x{0:x}".format(address))

        self.bus = bus
        self.address = address
        self.setup()
        # Set up MPU       
    
    def setup(self):
        config = [0x08, 0x00]
        self.bus.write_i2c_block_data(0x38, 0xE1, config)
        
        
    def read_raw_data(self):
    	#Accelero and Gyro value are 16-bit
        MeasureCmd = [0x33, 0x00]
        self.bus.write_i2c_block_data(0x38, 0xAC, MeasureCmd)
        return self.bus.read_i2c_block_data(0x38,0x00) #data
            
        
    def celsius(self):  
        data = self.read_raw_data()
        temp = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
        return ((temp*200) / 1048576) - 50
    
    
    def farenheit(self):
        return self.celsius() * (9/5) + 32
        
        
    def humidity(self):
        data = self.read_raw_data()
        hum = ((data[1] << 16) | (data[2] << 8) | data[3]) >> 4
        return int(hum * 100 / 1048576)
        
    def run(self, faren):
        while True:
            c = self.celsius()
            f = self.farenheit()
            h = self.humidity()
            if faren:
                return"T=%.2f" %f+u'\u00b0'+" RH=%.2f" %h
            else:
                return "T=%.2f" %c+u'\u00b0'+ " RH=%.2f" %h
            
    

if __name__ == '__main__':
    print (" Reading Data of Gyroscope and Accelerometer")

    temp = AHT10(smbus.SMBus(1), 0x38)
    
    while True:
        text = temp.run(False)
        print(text)
        sleep(.5)
    
    