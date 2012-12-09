import _HT16K33

class SevenSegment(_HT16K33.Base):
  TOP_BAR = 0x01
  MIDDLE_BAR = 0x40
  BOTTOM_BAR = 0x08
  LEFT_TOP_BAR = 0x20
  LEFT_BOTTOM_BAR = 0x10
  RIGHT_TOP_BAR = 0x02
  RIGHT_BOTTM_BAR = 0x04
  PERIOD = 0x80
  
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
  
  def getDigitAddressByIndex(self,index=0):
    return self.DIGIT_ADDRESS[int(index) % len(self.DIGIT_ADDRESS)]
  
  def setDigit(self,position=0,value=0x00):
    self.bus.write_byte_data(self.address,self.getDigitAddressByIndex(position),int(value) % 0x100)
    
  def chrToInt(self,character):
    integer=0x00
    try:
      integer=self.CHARACTER_MAP[ord(str(character)]
    except KeyError:
      pass
    return integer
  def readAtIndex(self,index=0):
    self.bus.read_byte_data(self.address,self.getDigitAddressByIndex(index))
  def turnOnColon(self):
    self.bus.write_byte_data(self.address,self.COLON_ADDRESS,0xFF)
  def turnOffColon(self):
    self.bus.write_byte_data(self.address,self.COLON_ADDRESS,0x00)
  