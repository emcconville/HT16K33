#!/bin/env python

# FourDigit - Thinking
# Indicate to user that the computer is working

from __future__ import print_function
import time

from .HT16K33 import FourDigit

# Enable device
digit = FourDigit(bus=0,address=0x70).setUp()

# Tell operator process has started
print("Starting HT16K33.FourDigit thinking...(Ctl-C to quit)")
while True: # Forever loop
  try:
    # Prototype multiplier
    cursor = 0x01
    # cursor is under-or-equal to 32
    while cursor <= 0x20:
      # Set digit in each position to current display
      for position in range(4):
        digit.setDigit(position,cursor)
      # Increment cursor
      cursor *= 0x02
      # Delay 1/10th second
      time.sleep(0.1)
  
  # Catch exit, and turn off device
  except (KeyboardInterrupt,SystemExit):
    print("terminating....", end="")
    digit.clear().turnOffOscillator()
    time.sleep(0.1)
    print("done")
    break
  # Anything else, quit forever loop
  except:
    break

