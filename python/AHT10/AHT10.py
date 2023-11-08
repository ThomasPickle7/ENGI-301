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
class HT16K33():
    """ Class to manage a HT16K33 I2C display """
    # Class variables
    bus     = None
    address = None
    command = None
    
    def __init__(self, bus, address=0x38):
        """ Initialize class variables; Set up display; Set display to blank """
        
        # Initialize class variable=
        print("AHT10:")
        print("    Bus     = {0}".format(bus))
        print("    Address = 0x{0:x}".format(address))

        self.bus = bus
        self.address = address
        self.command = "/usr/sbin/i2cset -y {0} {1}".format(bus, address)

        # Set up display        

        # Set display to blank
        
    def _setup(self):
        """ Setup the hardware components. """
        # Initialize Button
        # HW#4 TODO: (one line of code)
        #   Remove "pass" and use the Adafruit_BBIO.GPIO library to set up the button
        GPIO.setup(self.pin, GPIO.IN)