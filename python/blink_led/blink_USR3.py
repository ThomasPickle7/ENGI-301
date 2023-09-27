"""
--------------------------------------------------------------------------
Onboard USB Blinker
--------------------------------------------------------------------------
License:
Copyright 2021-2023 - <Your Name>
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
Button Driver
This driver is built for buttons that have a pull up resistor between the
button and the processor pin (i.e. the input is "High"/"1" when the button is
not pressed) and will be connected to ground when the button is pressed (i.e.
the input is "Low" / "0" when the button is pressed)
Software API:
Button(pin)
- Provide pin that the button monitors
is_pressed()
- Return a boolean value (i.e. True/False) on if button is pressed
- Function consumes no time
wait_for_press(function=None)
- Wait for the button to be pressed
- Optionally takes in an argument "function" which is the function
to be executed when waiting for the button to be pressed
- Function consumes time
- Returns a tuple:
(<time button was pressed>, <data returned by the "function" argument>)
"""

import Adafruit_BBIO.GPIO as GPIO
import time

GPIO.setup("USR3", GPIO.OUT)
freq = 5

while True:
    GPIO.output("USR3", GPIO.HIGH)
    time.sleep((1/freq)/2)
    GPIO.output("USR3", GPIO.LOW)
    time.sleep((1/freq)/2)