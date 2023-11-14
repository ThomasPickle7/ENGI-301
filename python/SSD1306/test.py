# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
HT16K33 I2C Library
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

  HT16K33(bus, address=0x70)
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
 
  * Using seven-segment digit LED display for Adafruit's HT16K33 I2C backpack:
    * http://adafruit.com/products/878
    * https://learn.adafruit.com/assets/36420
    * https://cdn-shop.adafruit.com/datasheets/ht16K33v110.pdf
    
    * Base code (adapted below):
        * https://github.com/emcconville/HT16K33/blob/master/FourDigit.py
        * https://github.com/emcconville/HT16K33/blob/master/_HT16K33.py
        * https://github.com/adafruit/Adafruit_Python_LED_Backpack/blob/master/Adafruit_LED_Backpack/HT16K33.py
        * https://github.com/adafruit/Adafruit_Python_LED_Backpack/blob/master/Adafruit_LED_Backpack/SevenSegment.py
        * https://github.com/adafruit/Adafruit_Python_LED_Backpack/blob/master/examples/sevensegment_test.py

    * Letters Supported from:
        * https://en.wikichip.org/wiki/seven-segment_display/representing_letters
        
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

# See https://en.wikipedia.org/wiki/Seven-segment_display for reference 

WIDTH = 128
HEIGHT = 32  # Change to 64 if needed
BORDER = 5


# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------
class SSD1306():
    """ Class to manage a HT16K33 I2C display """
    # Class variables
    
    
    def __init__(self, address=0x3c):
        """ Initialize class variables; Set up display; Set display to blank """
        
        # Initialize class variable=
        print("SSD1306")
        self.i2c = board.I2C()  # uses board.SCL and board.SDA
        self.oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, self.i2c, addr=0x3C, reset=None)
        
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
    
    def border(self):
        """ Update the value on the display with text
        
        :param value:  Value must have between 1 and 4 characters
        
        Will throw a ValueError if there are not the appropriate number of 
        characters or if characters are used that are not supported.
        """
        

# End class


# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    disp = SSD1306(0x3c)
    disp.update_text("Temp: 62.3F")
    sleep(3)
    disp.update_text("Humidity: 74%")



