#!/bin/env python

try:
    from smbus import SMBus
except ImportError:
    print '''
    \033[1;93m!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    \033[1;93m!\033[1;91m Unable to load SMBus            \033[1;93m!
    \033[1;93m!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    \033[1;93m!\033[0;91m Switching to terminal emulation \033[1;93m!
    \033[1;93m!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\033[0m
    '''
    import sys
    class SMBus(object):
        memory = {0:0, 2:0, 4:0, 6:0, 8:0, 10:0, 12:0, 14:0}
        debug = True
        def __init__(self,bus=0):
            self.bus = bus
            self.debug =  __name__ != "__main__" 
        def write_byte(self,address,byte):
            sys.stderr.write( "[%d:0x%0.2X] Writing byte 0x%0.2X\n" % (self.bus,address,byte) )
        def write_byte_data(self,address,byte,value):
            self.memory[byte] = value
            sys.stderr.write( "[%d:0x%0.2X] Setting byte 0x%0.2X value 0x%0.2X [%s]\n" % (self.bus,address,byte,value,bin(value)) )
        def read_byte_data(self,address,byte):
            sys.stderr.write( "[%d:0x%0.2X] Reading byte 0x%0.2X value 0x%0.2X [%s]\n" % (self.bus,address,byte,self.memory[byte],bin(self.memory[byte])) )
            return self.memory[byte]

class Device(object):
  
  bus=0x00
  address=0x70
  
  VERSION = "0.0.1"
  
  DISPLAY_ADDRESS=0x80
  BRIGHTNESS_ADDRESS=0xE0
  OSCILLATOR=0x21
  
  def __init__(self,**kwargs):
      if "address" in kwargs:
          self.address = kwargs["address"]
      if "bus" in kwargs:
          self.bus = kwargs["bus"]
      self.bus = SMBus(self.bus)
  
  def clear(self):
      '''
         Loop through all data addresses, and clear any LEDS
           
         Example:
         >>> bus = Base()
         >>> bus.clear()  # doctest: +ELLIPSIS
         <...Base object at 0x...>
      '''
      for i in range(0x10):
          self.bus.write_byte_data(self.address, i, 0x00)
      return self
  
  def setBrightness(self,brightness=0x0F):
      '''
         Set brightness level
         - brightness (0..15)
         --  0 =  1/16 duty
         --  1 =  2/16 duty
         --  2 =  3/16 duty
         --  3 =  4/16 duty
         --  4 =  5/16 duty
         --  5 =  6/16 duty
         --  6 =  7/16 duty
         --  7 =  8/16 duty
         --  8 =  9/16 duty
         --  9 = 10/16 duty
         -- 10 = 11/16 duty
         -- 11 = 12/16 duty
         -- 12 = 13/16 duty
         -- 13 = 14/16 duty
         -- 14 = 15/16 duty
         -- 15 = 16/16 duty
         
         Example:
         >>> bus = Base()
         >>> bus.setBrightness(15) # doctest: +ELLIPSIS
         <...Base object at 0x...>
      '''
      brightness = int(brightness) % 0x10
      self.bus.write_byte(self.address, self.BRIGHTNESS_ADDRESS | brightness )
      return self
  
  def setDisplay(self,on=True,blink_rate=0x00):
      '''
         Set display options
         - on (Boolean)
         - blink_rate (0..3)
         -- 0 = Blink off
         -- 1 = 2HZ
         -- 2 = 1HZ
         -- 3 = 0.5HZ
           
         Example:
         >>> bus = Base()
         >>> bus.setDisplay(True,4) #doctest: +ELLIPSIS
         <...Base object at 0x...>
      '''
      blink_rate = int(blink_rate) % 0x04
      on = int(on) % 0x02
      self.bus.write_byte( self.address, self.DISPLAY_ADDRESS | (blink_rate << 0x01) | on )
      return self
  
  def setUp(self,**kwargs):
    _defaults = {
      "display_on" : True, # Enable display
      "blink_rate" : 0x00, # Disable blink rate
      "brightness" : 0x07  # Default brightness to 8/16th duty
    }
    args = dict(_defaults.items() + kwargs.items())
    '''
       Clear & set default state of HT16K33 internal systems
       KeyWords:
       - display_on (Boolean, default True)
       - blink_rate (0x00..0x03, default 0x00)
       - brightness (0x00..0x0F, default 0x07)
       
       Example:
       >>> bus = Base().setUp()
    '''
    self.clear() # Clear out manufacturer's test message
    self.turnOnOscillator() # Start internal oscillator
    self.setDisplay(args["display_on"],args["blink_rate"])
    self.setBrightness(args["brightness"])
    return self
        
  def turnOnOscillator(self):
      '''
         Enable HT16K33 internal system oscillator
           
         Example:
         >>> bus = Base()
         >>> bus.turnOnOscillator() # doctest: +ELLIPSIS
         <...Base object at 0x...>
      '''
      self.bus.write_byte(self.address, self.OSCILLATOR)
      return self
    
  def turnOffOscillator(self):
      '''
         Disable HT16K33 internal system oscillator
           
         Example:
         >>> bus = Base()
         >>> bus.turnOffOscillator()  # doctest: +ELLIPSIS
         <...Base object at 0x...>
      '''
      self.bus.write_byte(self.address, self.OSCILLATOR^0x01)
      return self
  

if __name__ == "__main__":
    import doctest
    doctest.testmod()
