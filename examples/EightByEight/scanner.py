#!/bin/env python

# EightByEight - Scanner 
# An example of horizontal & vertical lines osculating accross a 8x8 field

from HT16K33 import EightByEight
import time

position  = 0 # Placement cursor
direction = 1 # Signed direction to increment (+/-)
matrix = EightByEight().setUp() # Init device
column_value = matrix.COLUMN_VALUES[position] # Assign first postion of column

# Inform user
print "Starting HT16K33.EightByEight scanner...(Ctl-C to quit)"
while True: # Forever loop
  try:
    # Loop through 8x8 field
    for row in range(0,8):
      # If matches position, show full horizontal line
      if row == position:
        matrix.setRow(row,0xFF) # 0xFF (or 255) is a full horizontal line
      else:
        # display column_value
        matrix.setRow(row,column_value)
    
    # Increment position based on direction
    position += (1*direction)
    
    # Get next column value
    column_value = matrix.COLUMN_VALUES[position]
    
    # Reverse direction if position meets bonds
    if position == 7:
      direction = -1
    elif position == 0:
      direction = 1
    
    # Delay for 1/16 sec; such that, one full rotation will occur per second
    time.sleep(0.0625)
  
  # Catch exit, and turn off device
  except (KeyboardInterrupt,SystemExit):
    print "terminating....",
    matrix.clear().turnOffOscillator()
    print "done"
    break
  # Anything else, quit forever loop
  except:
    print "Unknown expected exception..."
    break
