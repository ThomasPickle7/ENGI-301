"""
--------------------------------------------------------------------------
Simple Calculator
--------------------------------------------------------------------------
License:
Copyright 2023 - Thomas Pickell
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors
may be used to endorse or promote products derived from this software without
specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
Simple calculator that will
- Take in two numbers from the user
- Take in an operator from the user
- Perform the mathematical operation and provide the number to the user
- Repeat
Operations:
- "+" : addition
- "-" : subtraction
- "*" : multiplication
- "/" : division
Error conditions:
- Invalid operator --> Program should exit
- Invalid number --> Program should exit
--------------------------------------------------------------------------
"""
"""
Inputs:
button_start- a button which starts/stops the stopwatch from running
button_reset- a button which resets the stop watch
display- a display that shows the user their time

Outputs:
time- a set of integers which indicate elapsed time
"""
import time
class Stopwatch:
    def __init__(self, hours=0, minutes=0, seconds=0):
        self.hours = hours
        self. minutes = minutes
        self.seconds = seconds
        self.is_running = False
        # Establish the display, a lap/reset button, and a start/stop button+
    def update_time(self):
        if self.seconds == 60:
            self.minutes += 1
            self.seconds = 0
        if self.minutes == 60:
            self.hours += 1
            self.minutes = 0
    def print_time(self):
        print(self.hours, ":", self.minutes, ":", self.seconds) #Replace with display code
    def increment(self):
        if self.is_running:
            self.seconds += 1
            self.update_time()
    def turned_on(self, power):
        self.is_running = power

test_watch = Stopwatch()
test_watch.turned_on(True)
while True:
    time.sleep(.01)
    test_watch.increment()
    test_watch.print_time()




