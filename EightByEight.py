from _HT16K33 import Device


__all__ = ['EightByEight']


class EightByEight(Device):
    '''
       8x8 LED matrix for Adafruit's HT16K33 LED backpack
       - - -
       [1.2" Blue](https://www.adafruit.com/products/1052)
       [1.2" Green](https://www.adafruit.com/products/1051)
       [1.2" Red](https://www.adafruit.com/products/1049)
       [1.2" Yellow](https://www.adafruit.com/products/1050)
       [Mini Blue](https://www.adafruit.com/products/959)
       [Mini Green](https://www.adafruit.com/products/872)
       [Mini Red](https://www.adafruit.com/products/870)
       [Mini Ultra Bright White](https://www.adafruit.com/products/1080)
       [Mini Yellow](https://www.adafruit.com/products/871)
       - - -
    '''

    ROW_ADDRESS = [0x00, 0x02, 0x04, 0x06, 0x08, 0x0A, 0x0C, 0x0E]
    COLUMN_VALUES = [0x80, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40]

    def alterSingleLED(self, x, y, action=None):
        '''
           Manipulate single lead at point (x, y)
           - x = Column (0..7)
           - y = Row (0..7)
           - action = ("or","xor","andnot")

           Example:
           >>> matrix = EightByEight().setUp()
           >>> matrix.setRow(0, 0b11110000)
           >>> matrix.alterSingleLED(4, 0,"or")
           >>> matrix.alterSingleLED(4, 0,"xor")
           >>> matrix.alterSingleLED(7, 0,"andnot")
        '''
        x = int(x) % 8
        y = int(y) % 8
        row_address = self.getRowAddressByIndex(y)
        byte = self.bus.read_byte_data(self.address, row_address)
        new_byte = self.COLUMN_VALUES[x]
        if action == "or":
            byte |= new_byte
        elif action == "xor":
            byte ^= new_byte
        elif action == "andnot":
            byte &= ~new_byte
        else:
            byte = new_byte
        self.bus.write_byte_data(self.address, row_address, byte)

    def getRowAddressByIndex(self, row):
        '''
           Retrieve address of row by index.
           - row (0..7)

           Example:
           >>> EightByEight().getRowAddressByIndex(0x06)
           12
        '''
        return self.ROW_ADDRESS[int(row) % len(self.ROW_ADDRESS)]

    def setRow(self, row=0, columns=[]):
        '''
           Set LED status
           - row (0..7)
           - columns (mixed)
           -- 8 item list of booleans
           -- Unsigned intager
           --- 0..255
           --- 0x00..0xFF
           --- 0b00000000...0b11111111

           Example:
           - Display the following image
                + + - - - - - -
                + + + + - - - -
                + + + + + + - -
                + + + + + + + +
                + + + + + + + +
                + + + + + + - -
                + + + + - - - -
                + + - - - - - -
           >>> matrix=EightByEight().setUp()
           >>> matrix.setRow(0,[True, True])
           >>> matrix.setRow(1,[True, True, True, True])
           >>> matrix.setRow(2,[1, 1, 1, 1, 1, 1, 0, 0])
           >>> matrix.setRow(3, 0xFF)
           >>> matrix.setRow(4, 255)
           >>> matrix.setRow(5, 0b10011111)
           >>> matrix.setRow(6, 0x87)
           >>> matrix.setRow(7, 0x81)
        '''
        row_address = self.getRowAddressByIndex(row)
        value = 0
        if isinstance(columns, list):
            for index in columns:
                if index:
                    value |= self.COLUMN_VALUES[index]
        elif isinstance(columns, int):
            value = columns % 0x100
        self.bus.write_byte_data(self.address, row_address, value)

    def turnOnLED(self, x, y):
        '''
           Turn on single LED at x, y
           - x = Column (0..7)
           - y = Row (0..7)

           Example:
           >>> matrix = EightByEight().setUp()
           >>> matrix.setRow(0, 0)
           >>> matrix.turnOnLED(5, 0)
           >>> matrix.clear() #doctest: +SKIP
        '''
        self.alterSingleLED(x, y, "or")

    def turnOffLED(self, x, y):
        '''
           Turn off single LED at x, y
           - x = Column (0..7)
           - y = Row (0..7)

           Example:
           >>> matrix = EightByEight().setUp()
           >>> matrix.setRow(0, 0xFF)
           >>> matrix.turnOffLED(5, 0)
           >>> matrix.clear() #doctest: +SKIP
        '''
        self.alterSingleLED(x, y, "andnot")

    def toggleLED(self, x, y):
        '''
           Toggle off/on single LED at x, y
           - x = Column (0..7)
           - y = Row (0..7)

           Example:
           >>> matrix = EightByEight().setUp()
           >>> matrix.setRow(0, 0xFF) #doctest: +SKIP
           >>> matrix.toggleLED(7, 0)
           >>> matrix.toggleLED(6, 0)
           >>> matrix.toggleLED(5, 0)
           >>> matrix.toggleLED(6, 0)
           >>> matrix.toggleLED(7, 0)
           >>> matrix.clear() #doctest: +SKIP
        '''
        return self.alterSingleLED(x, y, "xor")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
