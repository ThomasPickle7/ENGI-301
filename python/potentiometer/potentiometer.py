"""
--------------------------------------------------------------------------
Potentiometer Driver
--------------------------------------------------------------------------
License:   
Copyright 2023 <NAME>

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

Potentiometer Driver for PocketBeagle

Software API:

  Potentiometer(pin)
    - Provide PocketBeagle pin that the potentiometer is connected

  get_value()
    - Returns the raw ADC value.  Integer in [0, 4095] 

  get_voltage()
    - Returns the approximate voltage of the pin in volts

"""
import Adafruit_BBIO.ADC as ADC

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

MIN_VALUE     = 0
MAX_VALUE     = 4095

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

PINS_3V6 = ["P1_2", "P2_35"]
PINS_1V8 = ["P1_19", "P1_21", "P1_23", "P1_25", "P1_27", "P2_36"]

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class Potentiometer():
    """ Button Class """
    pin             = None
    voltage         = None
    
    def __init__(self, pin=None, voltage=1.8):
        """ Initialize variables and set up the potentiometer """
        if (pin == None):
            raise ValueError("Pin not provided for Potentiometer()")
        else:
            self.pin = pin
            
        if pin in PINS_3V6:
            self.voltage = 3.6
        else:
            self.voltage = 1.8
            
            if pin not in PINS_1V8:
                print("WARNING:  Unknown pin {0}.  Setting voltage to 1.8V.".format(pin))
        
        # Initialize the hardware components        
        self._setup()
    
    # End def
    
    
    def _setup(self):
        """ Setup the hardware components. """
        # Initialize Analog Input

        ADC.setup()

    # End def


    def get_value(self):
        """ Get the value of the Potentiometer
        
           Returns:  Integer in [0, 4095]
        """
        # Read raw value from ADC

        return int(ADC.read_raw(self.pin))

    # End def

    
    def get_voltage(self):
        """ Get the voltage of the pin
        
           Returns:  Float in volts
        """
        return ((self.get_value() / MAX_VALUE) * self.voltage)
    
    # End def    
    
    
    def cleanup(self):
        """Cleanup the hardware components."""
        # Nothing to do for ADC
        pass        
        
    # End def

# End class



# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    import time

    print("Potentiometer Test")

    # Create instantiation of the potentiometer
    pot = Potentiometer("P1_19")

    # Use a Keyboard Interrupt (i.e. "Ctrl-C") to exit the test
    print("Use Ctrl-C to Exit")
    
    try:
        while(1):
            # Print potentiometer value
            print("Value   = {0}".format(pot.get_value()))
            print("Voltage = {0} V".format(pot.get_voltage()))
            time.sleep(1)
        
    except KeyboardInterrupt:
        pass

    print("Test Complete")

