#!/bin/env python

# FourDigit - Clock
# Display simple 24-hour clock

from HT16K33 import FourDigit
import time

# Enable device
digit = FourDigit(bus=0,address=0x70).setUp()

# Inform user of running process
print "Starting HT16K33.FourDigit clock...(Ctl-C to quit)"
while True: # Forever loop
  try:
    # Get string of 24-hour time
    display_digit = time.strftime("%H%M")
    
    # Loop through characters and keep index
    for index,item in enumerate(list(display_digit)):
      
      # Don't display "0" for first character
      if index == 0 and item != "0":
        digit.writeDigit(index,item)
      # Else (if not first character) write to device
      elif index != 0:
        digit.writeDigit(index,item)
    
    # Blink colon for a second
    digit.turnOffColon()
    time.sleep(1)
    digit.turnOnColon()
    time.sleep(1)
  
  # Catch exit, and turn off device
  except (KeyboardInterrupt,SystemExit):
    print "terminating....",
    digit.clear().turnOffOscillator()
    time.sleep(0.1)
    print "done"
    break
  # Anything else, quit forever loop
  except:
    break
      
      
