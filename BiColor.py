from ._HT16K33 import Device


__all__ = ['BiColor']


class BiColor(Device):
  '''
     BiColor 8x8 Matrix with Adafruit's I2C Backpack
     [Bicolor LED Square](https://www.adafruit.com/products/902)
  '''
  GREEN_COLUMN_ADDRESS=(0x0E, 0x0C, 0x0A, 0x08, 0x06, 0x04, 0x02, 0x00)
  RED_COLUMN_ADDRESS  =(0x0F, 0x0D, 0x0B, 0x09, 0x07, 0x05, 0x03, 0x01)
  ROW_VALUES=(0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80)

  def alterSingleLED(self, x, y, action, isRed=False):
    '''
       Manipulate single lead at point (x, y)
       - x = Column (0..7)
       - y = Row (0..7)
       - action = ("or","xor","andnot")
       - isRed = (Boolean, default=False)

       Example:
       >>> square = BiColor().setUp()
       >>> square.setColumn(0, 0b00001111, False)      # Top 4 LEDs green
       >>> square.setColumn(0, 0b11110000, True)       # Bottom 4 LEDs red
       >>> square.alterSingleLED(0, 4,"or", False)     # Top red LED set to yellow
       >>> square.alterSingleLED(0, 4,"xor", True)     # Same yellow set to green
       >>> square.alterSingleLED(0, 4,"andnot", False) # Turn off new green LED
    '''
    column_address = self.getColumnAddressByIndex(x, isRed)
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

  def getColumnAddressByIndex(self, column, isRed=False):
    '''
       Retrieve column address based on index & color
       - column (0..7)
       - isRed (Boolean, default=False)

       Example:
       >>> BiColor().getColumnAddressByIndex(2, True)  # Get 3rd column address (red)
       11
       >>> BiColor().getColumnAddressByIndex(2, False) # Get 3rd column address (green)
       10
    '''
    column = int(column) % 0x08
    return self.RED_COLUMN_ADDRESS[column] if isRed else self.GREEN_COLUMN_ADDRESS[column]

  def getRowValue(self, position=0x00):
    '''
       Retrieve value of row position
       - position (0..7)

       Example:
       >>> BiColor().getRowValue(1)
       2
       >>> BiColor().getRowValue(11)
       8
    '''
    return self.ROW_VALUES[int(position) % 0x08]

  def setColumn(self, column=0, value=0x00, isRed=False):
    '''
       Assign all LEDs in a given column

       - column (0..7)
       - value (0x00..0xFF)
       - isRed (Boolean, default=False)

       Example:
       >>> square = BiColor().setUp()
       >>> for i in range(8):
       ...  square.setColumn(i, 0xFF, False)
       ...
    '''
    column_address=self.getColumnAddressByIndex(column, isRed)
    value=int(value) % 0x100
    self.bus.write_byte_data(self.address, column_address, value)

  def turnOnGreenLED(self, x, y):
    '''
       Turn on single green LED at x, y
       - x (0..7)
       - y (0..7)
    '''
    self.alterSingleLED(x, y,"or", False)

  def turnOffGreenLED(self, x, y):
    '''
       Turn off single green LED at x, y
       - x (0..7)
       - y (0..7)
    '''
    self.alterSingleLED(x, y,"andnot", False)

  def toggleGreenLED(self, x, y):
    '''
       Toggle single green LED at x, y
       - x (0..7)
       - y (0..7)
    '''
    self.alterSingleLED(x, y,"xor", False)

  def turnOnRedLED(self, x, y):
    '''
       Turn on single red LED at x, y
       - x (0..7)
       - y (0..7)
    '''
    self.alterSingleLED(x, y,"or", True)

  def turnOffRedLED(self, x, y):
    '''
       Turn off single red LED at x, y
       - x (0..7)
       - y (0..7)
    '''
    self.alterSingleLED(x, y,"andnot", True)

  def toggleRedLED(self, x, y):
    '''
       Toogle single red LED at x, y
       - x (0..7)
       - y (0..7)
    '''
    self.alterSingleLED(x, y,"xor", True)

  def turnOffLED(self, x, y):
    '''
       Turn off both green & red LEDs at point x, y
       - x (0..7)
       - y (0..7)
    '''
    self.turnOffGreenLED(x, y)
    self.turnOffRedLED(x, y)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
