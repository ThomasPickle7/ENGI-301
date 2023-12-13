# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Threading Example 
--------------------------------------------------------------------------
License:   
Copyright 2020-2023 - <Name>

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
Python Threading Example
  - Create threading class that takes in an argument
  - Class run method will print that it started; sleep a random amount of time;
    and print when it ends

"""
import time
import random
import threading

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------


# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class MyThreadWithArgs(threading.Thread):
    arg = None

    def __init__(self, arg):
        """Class initialization method"""
        # Call parent initialization

        # Assign class variables
        self.arg   = arg
    # End def

    def run(self):
        """ Class run method
                Called automatically when a new thread is started.
        """
        print("Run  : {0} with arg = {1}".format(self.name, self.arg))
        time.sleep(5 * random.random())
        print("Done : {0}".format(self.name))
        
        return
    # End def

# End class


# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    # Start Threads
    for i in range(5):
        print("Start thread {0}".format(i))
        
        # Create thread with argument i

        # Start Thread


    # Stop Threads
    # Get main thread 
    main_thread = None  # NEED TO CHANGE

    for t in threading.enumerate():
        if t is not main_thread:
            # Join threads 
            t.join()














































































































































































