# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
SSD1306 I2C Library
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

  SSD1306(bus, address=0x70)
    - Provide i2c bus that dispaly is on
    - Provide i2c address for the display
    
    blank()
      - Clears the display
    
    update_text(text)
      - Writes text in the center of the display

    
  
------------------------------------------------------------------------
        
"""
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from time import sleep

# Define the Reset Pin
oled_reset = None

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

WIDTH = 128
HEIGHT = 32  # Change to 64 if needed
BORDER = 5


# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------
class SSD1306():
    # Class variables
    
    
    def __init__(self, address=0x3c):
        """ Initialize class variables; Set up display; Set display to blank """
        
        # Initialize class variable=
        print("SSD1306")
        self.i2c = board.I2C()  # uses board.SCL and board.SDA
        self.oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, self.i2c, addr=0x3C, reset=None)
        
        #creates an image that will be drawn on the LCD Screen
        self.image = Image.new("1", (self.oled.width, self.oled.height))
        self.draw = ImageDraw.Draw(self.image)



      


    def blank(self):
        """Clear the display to read nothing"""
        self.oled.fill(0)
        self.oled.show()    
    
    # End def



    def update_text(self, text):
        """Update the value on the display.  
        
        This function will write charachters in a defualt font on the OLED display
        """
        self.draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)
        
        font = ImageFont.load_default()
        (font_width, font_height) = font.getsize(text)
        self.draw.text(
            (self.oled.width // 2 - font_width // 2, self.oled.height // 2 - font_height // 2),
            text,
            font=font,
            fill=255,
        )
        self.oled.image(self.image)
        self.oled.show()
    
            
            
            
    # End def
    
        

# End class


# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    disp = SSD1306(0x3c)
    disp.update_text("Temp: 62.3F")
    sleep(3)
    disp.update_text("Humidity: 74%")



