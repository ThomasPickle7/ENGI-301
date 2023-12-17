"""
--------------------------------------------------------------------------
MPU6050 I2C Library
--------------------------------------------------------------------------
License:   
Copyright 2018-2023 Thomas Pickell

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

  MPU6050(bus, address=0x68)
    - Provide i2c bus that dispaly is on
    - Provide i2c address for the display
    
    MPU_init()
      - Sets value of display to "0000"
    
    read_raw_data(addr)
      - Turns off all LEDs on display
    
    accel(enable)
      - Turns on / off the colon on the display.  Enable must be True/False.
    
    gyro()
      - Update the value on the display.  Value must be between 0 and 9999.

    gMag(value)
      - Update the value on the display with text.
        The following characters are supported:
            "abcdefghijlnopqrstuyABCDEFGHIJLNOPQRSTUY? -"
  
--------------------------------------------------------------------------
Background Information: 
 
  
"""
import smbus	#import SMBus module of I2C
import math
from time import sleep 

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47


class MPU6050:
    step_count = 0
    prev_mag = 0
    def __init__(self, bus, address=0x68):
        """ Initialize class variables; Set up display; Set display to blank """
        
        # Initialize class variable=
        print("MPU6050:")
        print("    Bus     = {0}".format(bus))
        print("    Address = 0x{0:x}".format(address))
        self.bus = bus
        self.address = address

        # Set up MPU       
        self.MPU_Init()
    
    def MPU_Init(self):
    	#write to sample rate register
    	self.bus.write_byte_data(self.address, SMPLRT_DIV, 7)
    	
    	#Write to power management register
    	self.bus.write_byte_data(self.address, PWR_MGMT_1, 1)
    	
    	#Write to Configuration register
    	self.bus.write_byte_data(self.address, CONFIG, 0)
    	
    	#Write to Gyro configuration register
    	self.bus.write_byte_data(self.address, GYRO_CONFIG, 24)
    	
    	#Write to interrupt enable register
    	self.bus.write_byte_data(self.address, INT_ENABLE, 1)
    
    def read_raw_data(self, addr):
    	#Accelero and Gyro value are 16-bit
            high = self.bus.read_byte_data(self.address, addr)
            low = self.bus.read_byte_data(self.address, addr+1)
        
            #concatenate higher and lower value
            value = ((high << 8) | low)
            
            #to get signed value from mpu6050
            if(value > 32768):
                    value = value - 65536
            return value
            
    def accel(self):
        
        """
        returns the acceleration vectors of the gyro
        """
        return [self.read_raw_data(ACCEL_XOUT_H) / 16384.0, self.read_raw_data(ACCEL_YOUT_H) / 16384.0, self.read_raw_data(ACCEL_ZOUT_H) / 16384.0,]
        
    def gyro(self):
        
        """
        returns the acceleration vectors of the gyro
        """
        return [self.read_raw_data(GYRO_XOUT_H) / 16384.0, self.read_raw_data(GYRO_YOUT_H) / 16384.0, self.read_raw_data(GYRO_ZOUT_H) / 16384.0,]
    
    def gMag(self):
        """
        returns the magnitude of the gyro vectors
        """
        
        Ax, Ay, Az = self.accel()
        Gx, Gy, Gz = self.gyro()
        return math.sqrt(Gx * Gx + Gy * Gy + Gz * Gz)
    def run(self):
        """
        determines whether or not a step has been made
        """
        
        while True:
    	
    	
    	    #Read Accelerometer raw value
    	    acc_x = self.read_raw_data(ACCEL_XOUT_H)
    	    acc_y = self.read_raw_data(ACCEL_YOUT_H)
    	    acc_z = self.read_raw_data(ACCEL_ZOUT_H)
    	
    	    #Read Gyroscope raw value
    	    gyro_x = self.read_raw_data(GYRO_XOUT_H)
    	    gyro_y = self.read_raw_data(GYRO_YOUT_H)
    	    gyro_z = self.read_raw_data(GYRO_ZOUT_H)
    	
    	    #Full scale range +/- 250 degree/C as per sensitivity scale factor
    	    Ax, Ay, Az = self.accel()
    	
    	    Gx, Gy, Gz = self.gyro()
    	
    	    Amag = self.gMag()
    	
    	
    	    if (self.prev_mag > Amag + .01 and self.prev_mag > .02):
    		    self.step_count += 1
    	    self.prev_mag = Amag
    	    return self.step_count	
    	    

if __name__ == '__main__':
    print (" Reading Data of Gyroscope and Accelerometer")
    
    gyro = MPU6050(smbus.SMBus(1), 0x68)
    while(True):
        var = gyro.run()
        print(var)
        sleep(.3)
    
