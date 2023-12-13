"""
--------------------------------------------------------------------------
Threaded Button Driver
--------------------------------------------------------------------------
License:   
Copyright 2023 - Erik Welsh

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

Threaded Button Driver

  This driver provides a button that runs in its own execution thread.
  

Software API:

  ThreadedButton(pin, sleep_time=0.1, active_high=True)
    - Provide pin that the button monitors
    - The sleep_time is the time between calls to the callback functions
      while the button is waiting in either the pressed or unpressed state
    - By default, the button is "active_high" (i.e. the button has a 
      pull up resistor between the button and the processor pin and 
      will be connected to ground when the button is pressed.  The 
      input is "High"/"1" when the button is not pressed, and the 
      input is "Low" / "0" when the button is pressed).  If false, 
      the button has the opposite polarity.
    
    start()
      - Starts the button thread
    
    is_pressed()
      - Return a boolean value (i.e. True/False) on if button is pressed
      - Function consumes no time
    
    get_last_press_duration()
      - Return the duration the button was last pressed

    cleanup()
      - Stops the button so thread can exit
      
    Callback Functions:
      These functions will be called at the various times during a button 
      press cycle.  There is also a corresponding function to get the value
      from each of these callback functions in case they return something.
    
      - set_pressed_callback(function)
        - Excuted every "sleep_time" while the button is pressed
      - set_unpressed_callback(function)
        - Excuted every "sleep_time" while the button is unpressed
      - set_on_press_callback(function)
        - Executed once when the button is pressed
      - set_on_release_callback(function)
        - Executed once when the button is released
      
      - get_pressed_callback_value()
      - get_unpressed_callback_value()
      - get_on_pressed_callback_value()
      - get_on_release_callback_value()      

"""
import time
import threading

import Adafruit_BBIO.GPIO as GPIO

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

HIGH          = GPIO.HIGH
LOW           = GPIO.LOW

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

# None

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class ThreadedButton(threading.Thread):
    """ Threaded Button Class """
    pin                           = None

    unpressed_value               = None
    pressed_value                 = None

    sleep_time                    = None
    stop_button                   = None
    press_duration                = None

    pressed_callback              = None
    pressed_callback_value        = None
    unpressed_callback            = None
    unpressed_callback_value      = None
    on_press_callback             = None
    on_press_callback_value       = None
    on_release_callback           = None
    on_release_callback_value     = None
    
    def __init__(self, pin=None, sleep_time=0.1, active_high=True):
        """ Initialize variables and set up the button """
        # Call parent class constructor
        threading.Thread.__init__(self)
        
        # Initialize the pin
        if (pin == None):
            raise ValueError("Pin not provided for Button()")
        else:
            self.pin = pin

        # Set pressed vs unpressed values            
        if active_high:
            self.unpressed_value = HIGH
            self.pressed_value   = LOW
        else:
            self.unpressed_value = LOW
            self.pressed_value   = HIGH

        # Initialize Class Variables      
        self.sleep_time      = sleep_time
        self.stop_button     = False
        self.press_duration  = 0.0

        # All callback functions and values set to None if not used        
        
        # Initialize the hardware components        
        self._setup()
    
    # End def
    
    
    def _setup(self):
        """ Setup the hardware components. """
        # Initialize Button
        GPIO.setup(self.pin, GPIO.IN)

    # End def


    def is_pressed(self):
        """ Is the Button pressed?
        
           Returns:  True  - Button is pressed
                     False - Button is not pressed
        """
        return GPIO.input(self.pin) == self.pressed_value

    # End def


    def run(self):
        """ Run the button thread.  Execute callbacks as appropriate. """
        function_return_value = None
        button_press_time     = None

        # Run button monitor until told to stop        
        while(not self.stop_button):
        
            # Wait for button press
            #   Execute the unpressed callback function based on the sleep time
            while(GPIO.input(self.pin) == self.unpressed_value):
            
                if self.unpressed_callback is not None:
                    self.unpressed_callback_value = self.unpressed_callback()
                
                if self.stop_button:
                    break
                
                time.sleep(self.sleep_time)
            
            # Record time
            button_press_time = time.time()
            
            # Executed the on press callback function
            if self.on_press_callback is not None:
                self.on_press_callback_value = self.on_press_callback()
            
            # Wait for button release
            #   Execute the pressed callback function based on the sleep time
            while(GPIO.input(self.pin) == self.unpressed_value):
            
                if self.pressed_callback is not None:
                    self.pressed_callback_value = self.pressed_callback()
                    
                if self.stop_button:
                    break
                    
                time.sleep(self.sleep_time)
            
            # Record the press duration
            self.press_duration = time.time() - button_press_time

            # Executed the on release callback function
            if self.on_release_callback is not None:
                self.on_release_callback_value = self.on_release_callback()        
        
        # Set the flag and press duration to allow the button thread to restart
        self.stop_button    = False
        self.press_duration = 0.0
        
    # End def

    
    def get_last_press_duration(self):
        """ Return the last press duration """
        return self.press_duration
    
    # End def
    
    
    def cleanup(self):
        """ Clean up the button hardware. """
        # Nothing to do for GPIO; stop the thread and wait for completion
        
        self.stop_button = True
        
        while (self.stop_button):
            time.sleep(self.sleep_time)
    
    # End def
    
    
    # -----------------------------------------------------
    # Callback Functions
    # -----------------------------------------------------

    def set_pressed_callback(self, function):
        """ Function excuted every "sleep_time" while the button is pressed """
        self.pressed_callback = function
    
    # End def

    def get_pressed_callback_value(self):
        """ Return value from pressed_callback function """
        return self.pressed_callback_value
    
    # End def
    
    def set_unpressed_callback(self, function):
        """ Function excuted every "sleep_time" while the button is unpressed """
        self.unpressed_callback = function
    
    # End def

    def get_unpressed_callback_value(self):
        """ Return value from unpressed_callback function """
        return self.unpressed_callback_value
    
    # End def

    def set_on_press_callback(self, function):
        """ Function excuted once when the button is pressed """
        self.on_press_callback = function
    
    # End def

    def get_on_press_callback_value(self):
        """ Return value from on_press_callback function """
        return self.on_press_callback_value
    
    # End def

    def set_on_release_callback(self, function):
        """ Function excuted once when the button is released """
        self.on_release_callback = function
    
    # End def

    def get_on_release_callback_value(self):
        """ Return value from on_release_callback function """
        return self.on_release_callback_value
    
    # End def    
    
# End class



# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    """ This test requires the use of two LEDs as well as two buttons.
    
    In this test there are two threaded buttons running in parallel.  Each
    button controls an LED.  When the button is pressed, the corresponding 
    LED will turn on and when the button is released, the LED will turn off.
    """
    import sys

    # Update path to correct directory for LED class     
    sys.path.append("/var/lib/cloud9/ENGI301/python/led")
    
    print("Threaded Button Test")

    # Create instantiation of the buttons and LEDs
    button_0 = ThreadedButton("P2_2")
    button_1 = ThreadedButton("P2_8")

    try:
        # Set up the LEDs
        import led as LED
        
        led_0    = LED.LED("P2_4")
        led_1    = LED.LED("P2_6")

        # Set up the button callbacks
        button_0.set_on_press_callback(led_0.on)
        button_0.set_on_release_callback(led_0.off)
        
        button_1.set_on_press_callback(led_1.on)
        button_1.set_on_release_callback(led_1.off)
        
    except:
        # LEDs not available, use print statements instead
        def led_0_on():
            print("LED 0: ON")
        def led_0_off():
            print("LED 0: OFF")
        def led_1_on():
            print("LED 1: ON")
        def led_1_off():
            print("LED 1: OFF")
            
        # Set up the button callbacks
        button_0.set_on_press_callback(led_0_on)
        button_0.set_on_release_callback(led_0_off)
        
        button_1.set_on_press_callback(led_1_on)
        button_1.set_on_release_callback(led_1_off)
    
    # Start the buttons
    button_0.start()
    button_1.start()
    
    # Get the main thread
    main_thread = threading.currentThread()
    
    # Use a Keyboard Interrupt (i.e. "Ctrl-C") to exit the test
    try:
        while (True):
            # Do nothing in the main thread
            time.sleep(1)
        
    except KeyboardInterrupt:
        # Clean up the hardware
        button_0.cleanup()
        button_1.cleanup()

        try:
            led_0.cleanup()
            led_1.cleanup()
        except:
            pass

    # Wait for threads to complete        
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()

    print("Test Complete")

