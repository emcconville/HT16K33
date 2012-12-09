import _HT16K33

class BiColor(_HT16K33.Base):
  
  GREEN_COLUMN_ADDRESS=(0x0E,0x0C,0x0A,0x08,0x06,0x04,0x02,0x00)
  RED_COLUMN_ADDRESS  =(0x0F,0x0D,0x0B,0x09,0x07,0x05,0x03,0x01)
  ROW_VALUES=(0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80)
  
  def alterSingleLED(self,x,y,action,isRed=False):
    column_address = self.getColumnAddressByIndex(x,isRed)
    new_byte = self.getRowValue(y)
    byte = self.bus.read_byte_data(self.address, column_address)
    if action == "or":
        byte |= new_byte
    elif action == "xor":
        byte ^= new_byte
    elif action == "andnot":
        byte &= ~new_byte
    else:
        byte = new_byte
    self.bus.write_byte_data(self.address, column_address, byte)
    
  def getColumnAddressByIndex(self,column,isRed=False):
    column = int(column) % 0x08
    return self.RED_COLUMN_ADDRESS[column] if isRed else self.GREEN_COLUMN_ADDRESS[column]
  def getRowValue(self,position=0x00):
    return self.ROW_VALUES[int(position) % 0x08]
  def setColumn(self,column=0,value=0x00,isRed=False):
    column_address=self.getColumnAddressByIndex(column,isRed)
    value=int(value) % 0x100
    self.bus.write_byte_data(self.address,column_address,value)
  def turnOnGreenLED(self,x,y):
    self.alterSingleLED(x,y,"or",False)
  def turnOffGreenLED(self,x,y):
    self.alterSingleLED(x,y,"andnot",False)
  def toggleGreenLED(self,x,y):
    self.alterSingleLED(x,y,"xor",False)
  def turnOnRedLED(self,x,y):
    self.alterSingleLED(x,y,"or",True)
  def turnOffRedLED(self,x,y):
    self.alterSingleLED(x,y,"andnot",True)
  def toggleRedLED(self,x,y):
    self.alterSingleLED(x,y,"xor",True)
  def turnOffLED(self,x,y):
    self.turnOffGreenLED(x,y)
    self.turnOffRedLED(x,y)
