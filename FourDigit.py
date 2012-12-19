import _HT16K33

class FourDigit(_HT16K33.Device):
  '''
     Four seven-segment digit LED display for Adafruit's HT16K33 I2C backpack
     - - -
     [Blue](http://adafruit.com/products/881)
     [Green](http://adafruit.com/products/880)
     [Red](http://adafruit.com/products/878)
     [Yellow](http://adafruit.com/products/879)
     [White](http://adafruit.com/products/1002)
  '''
  
  TOP_BAR          = 0x01
  MIDDLE_BAR       = 0x40
  BOTTOM_BAR       = 0x08
  LEFT_TOP_BAR     = 0x20
  LEFT_BOTTOM_BAR  = 0x10
  RIGHT_TOP_BAR    = 0x02
  RIGHT_BOTTOM_BAR = 0x04
  PERIOD           = 0x80
  
  DIGIT_ADDRESS = [0x00,0x02,0x06,0x08]
  COLON_ADDRESS = 0x04
  
  CHARACTER_MAP = {
    0x30 : 0x3F, # 0
    0x31 : 0x06, # 1
    0x32 : 0x5B, # 2
    0x33 : 0x4F, # 3
    0x34 : 0x66, # 4
    0x35 : 0x6d, # 5
    0x36 : 0x7d, # 6
    0x37 : 0x07, # 7
    0x38 : 0x7F, # 8
    0x39 : 0x67  # 9
  }
  
  def alterSingleLED(self,position=0,new_byte=0x00,action=None):
    '''
       Manipulate single LED in character position
       - position (0..3)
       - new_byte (0..0xFF)
       - action   ("or","xor","andnot")
       
       Example:
       >>> digit = FourDigit().setUp()    # Set-up
       >>> digit.setDigit(0,0x5B)            # Assign "2" character to first digit
       >>> digit.alterSingleLED(0,0x80,"or") # Alter first digit to include period
    '''
    position=int(position) % 4
    digit_address = self.getDigitAddressAtPosition(position)
    byte = self.bus.read_byte_data(self.address,digit_address)
    if action == "or":
        byte |= new_byte
    elif action == "xor":
        byte ^= new_byte
    elif action == "andnot":
        byte &= ~new_byte
    else:
        byte = new_byte
    self.bus.write_byte_data(self.address, digit_address, byte)
  
  def getDigitAddressAtPosition(self,position=0):
    '''
      Retrive address by position
      - position (0..3) 
      
      Example:
      >>> digit = FourDigit()
      >>> digit.getDigitAddressAtPosition(1)
      2
    '''
    return self.DIGIT_ADDRESS[int(position) % len(self.DIGIT_ADDRESS)]
  
  def chrToInt(self,character):
    '''
       Convert character to LED display integer
       
       Each available character will have the LED display
       integer assigned to the CHARACTER_MAP key matching
       character's order. Any character not present in 
       CHARACTER_MAP will return 0x00 (clear LED integer.)
       
       - character (see CHARACTER_MAP)
       
       Example:
       >>> digit = FourDigit().setUp()
       >>> digit.chrToInt(8)
       127
       >>> digit.chrToInt("T")
       0
    '''
    integer=0x00
    try:
      integer=self.CHARACTER_MAP[ord(str(character))]
    except KeyError:
      pass
    return integer
  
  def readAtPosition(self,position=0):
    '''
       Return LED value currently in devices EEPROM
       - position (0..3)
       
       Example:
       >>> digit = FourDigit().setUp()
       >>> digit.setDigit(0,0xFF)
       >>> digit.readAtPosition(0)
       255
    '''
    return self.bus.read_byte_data(self.address,self.getDigitAddressAtPosition(position))
  
  def setDigit(self,position=0,value=0x00):
    '''
       Assign LED display to digit
       - position
       - value
       
       Example:
       >>> digit = FourDigit().setUp()
       >>> digit.setDigit(0,0x06) # 1
       >>> digit.setDigit(1,0x5B) # 2
       >>> digit.setDigit(2,0x4F) # 3
       >>> digit.setDigit(3,0x66) # 4
    '''
    self.bus.write_byte_data(self.address,self.getDigitAddressAtPosition(position),int(value) % 0x100)
  
  def turnOnColon(self):
    '''
       Enable colon symbol
       
       Example:
       >>> digit = FourDigit().setUp()
       >>> digit.turnOnColon()
    '''
    self.bus.write_byte_data(self.address,self.COLON_ADDRESS,0xFF)
  
  def turnOffColon(self):
    '''
       Disable colon symbol
       
       Example:
       >>> digit = FourDigit().setUp()
       >>> digit.turnOffColon()
    '''
    self.bus.write_byte_data(self.address,self.COLON_ADDRESS,0x00)
  
  def turnOnPeriodAtPosition(self,position=0):
    '''
       Enable period symbol at given position
    '''
    self.alterSingleLED(position,self.PERIOD,"or")
  
  def turnOffPeriodAtPosition(self,position=0):
    '''
       Disable period symbol at given position
    '''
    self.alterSingleLED(position,self.PERIOD,"andnot")
  
  def writeDigit(self,position,char=None):
    '''
       Write single character to a given postion
       
       Example:
       >>> digit = FourDigit().setUp()
       >>> for i in range(4):
       ...   digit.writeDigit(i,i)
    '''
    self.setDigit(position,self.chrToInt(char))
  

if __name__ == "__main__":
    import doctest
    doctest.testmod()