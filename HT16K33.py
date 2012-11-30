#!/bin/env python

import time

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
    class SMBus(object):
        memory = {0:0, 2:0, 4:0, 6:0, 8:0, 10:0, 12:0, 14:0}
        debug = True
        def __init__(self,bus=0):
            self.bus = bus
            self.debug =  __name__ != "__main__" 
        def write_byte(self,address,byte):
            if self.debug:
                print "[%d:0x%x] Writing byte 0x%x" % (self.bus,address,byte)
        def write_byte_data(self,address,byte,value):
            self.memory[byte] = value
            if self.debug:
                print "[%d:0x%x] Setting byte 0x%x value 0x%x [%s]" % (self.bus,address,byte,value,bin(value))
        def read_byte_data(self,address,byte):
            if self.debug:
                print "[%d:0x%x] Reading byte 0x%x value 0x%x [%s]" % (self.bus,address,byte,self.memory[byte],bin(self.memory[byte]))
            return self.memory[byte]
    

class EightByEight(object):
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
    
    bus=0x00
    address=0x70
    
    DISPLAY_ADDRESS=0x80
    BRIGHTNESS_ADDRESS=0xE0
    OSCILLATOR=0x21
    ROW_ADDRESS=range(0x00,0x0F,0x02)
    COLUMN_VALUES=[0x80,0x01,0x02,0x04,0x08,0x10,0x20,0x40]
    
    def __init__(self,**kwargs):
        if 'address' in kwargs:
            self.address = kwargs['address']
        if 'bus' in kwargs:
            self.bus = kwargs['bus']
        self.bus = SMBus(self.bus)
    
    def alterSingleLED(self,x,y,action=None):
        '''
           Manipulate single lead at point (x,y)
           - x = Column (0..7)
           - y = Row (0..7)
           - action = ("or","xor","andnot")
           
           Example:
           >>> matrix = EightByEight().setUp()
           >>> matrix.clear() # doctest: +SKIP
           >>> matrix.setRow(0,0b11110000)
           >>> matrix.alterSingleLED(4,0,"or")
           >>> matrix.alterSingleLED(4,0,"xor")
           >>> matrix.alterSingleLED(7,0,"andnot")
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
    
    def clear(self):
        '''
           Loop through all rows, and clear any LEDS
           
           Example:
           >>> matrix = EightByEight()
           >>> matrix.clear()  # doctest: +ELLIPSIS
           <...EightByEight object at 0x...>
        '''
        for i in self.ROW_ADDRESS:
            self.bus.write_byte_data(self.address, i, 0x00)
        return self
    
    def getRowAddressByIndex(self,row):
        '''
           Retrieve address of row by index. Expects int 0 through 7 
           
           Row index out of range will return address matching modulus.
           
           Example:
           >>> EightByEight().getRowAddressByIndex(0x06)
           12
        '''
        return self.ROW_ADDRESS[int(row) % len(self.ROW_ADDRESS)]
    
    def setBrightness(self,brightness=0x0F):
        '''
           Set brightness level
           -  0 =  1/16 duty
           -  1 =  2/16 duty
           -  2 =  3/16 duty
           -  3 =  4/16 duty
           -  4 =  5/16 duty
           -  5 =  6/16 duty
           -  6 =  7/16 duty
           -  7 =  8/16 duty
           -  8 =  9/16 duty
           -  9 = 10/16 duty
           - 10 = 11/16 duty
           - 11 = 12/16 duty
           - 12 = 13/16 duty
           - 13 = 14/16 duty
           - 14 = 15/16 duty
           - 15 = 16/16 duty
           
           Example:
           >>> matrix = EightByEight()
           >>> matrix.setBrightness(15) # doctest: +ELLIPSIS
           <...EightByEight object at 0x...>
        '''
        brightness = int(brightness) % 0x10
        self.bus.write_byte(self.address, self.BRIGHTNESS_ADDRESS | brightness )
        return self
    
    def setDisplay(self,on=True,blink_rate=0x00):
        '''
           Set display options
           
           Apply system oscillator to LEDs.
           
           Expected `on`
           - False = Off
           - True = On
           
           Expected `blink_rate`
           - 0 = Blink off
           - 1 = 2HZ
           - 2 = 1HZ
           - 3 = 0.5HZ
           
           Example:
           >>> matrix = EightByEight()
           >>> matrix.setDisplay(True,4) #doctest: +ELLIPSIS
           <...EightByEight object at 0x...>
        '''
        blink_rate = int(blink_rate) % 0x04
        on = int(on) % 0x02
        self.bus.write_byte( self.address, self.DISPLAY_ADDRESS | (blink_rate << 0x01) | on )
        return self
    
    def setRow(self,row=0,columns=[]):
        '''
           Set LED status
           
           Expected row (0..7)
           Expected columns
           - 8 item list of booleans
           - Unsigned intager
           -- 0..255
           -- 0x00..0xFF
           -- 0b00000000...0b11111111
           
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
           >>> matrix.setRow(0,[True,True])
           >>> matrix.setRow(1,[True,True,True,True])
           >>> matrix.setRow(2,[1,1,1,1,1,1,0,0])
           >>> matrix.setRow(3,0xFF)
           >>> matrix.setRow(4,255)
           >>> matrix.setRow(5,0b10011111)
           >>> matrix.setRow(6,0x87)
           >>> matrix.setRow(7,0x81)
        '''
        row_address=self.getRowAddressByIndex(row)
        value=0
        if isinstance(columns,list):
            c = list(columns)
            while len(c) < 8:
                c.append(False)
            for index in range(0,8):
                if c[index]:
                    value |= self.COLUMN_VALUES[index]
        elif isinstance(columns,int):
            if columns > 0xFF :
                columns = 0xFF
            elif columns < 0x00 :
                columns = 0x00
            value = columns
        self.bus.write_byte_data(self.address, row_address, value)
        
    def setUp(self):
        '''
           Clear & set default state of HT16K33 internal systems
           
           - Blink disabled
           - Brightness 8/16 duty (half-dim)
           - All LEDS off
           
           Example:
           >>> matrix = EightByEight().setUp()
        '''
        self.clear() # Clear out manufacturer's test message
        self.turnOnOscillator() # Start internal oscillator
        self.setDisplay() # Enable display with no blink rates
        self.setBrightness(0x07) # Default to 8/16 brightness
        return self
        
    def turnOnOscillator(self):
        '''
           Enable HT16K33 internal system oscillator
           
           Example:
           >>> matrix = EightByEight()
           >>> matrix.turnOnOscillator() # doctest: +ELLIPSIS
           <...EightByEight object at 0x...>
        '''
        self.bus.write_byte(self.address, self.OSCILLATOR)
        return self
    
    def turnOffOscillator(self):
        '''
           Disable HT16K33 internal system oscillator
           
           Example:
           >>> matrix = EightByEight()
           >>> matrix.turnOffOscillator()  # doctest: +ELLIPSIS
           <...EightByEight object at 0x...>
        '''
        self.bus.write_byte(self.address, self.OSCILLATOR^0x01)
        return self
    
    def turnOnLED(self,x,y):
        '''
           Turn on single LED at x,y
           - x = Column (0..7)
           - y = Row (0..7)
           
           Example:
           >>> matrix = EightByEight().setUp()
           >>> matrix.setRow(0,0)
           >>> matrix.turnOnLED(5,0)
           >>> matrix.clear() #doctest: +SKIP
        '''
        self.alterSingleLED(x,y,"or")
    
    def turnOffLED(self,x,y):
        '''
           Turn off single LED at x,y
           - x = Column (0..7)
           - y = Row (0..7)
           
           Example:
           >>> matrix = EightByEight().setUp()
           >>> matrix.setRow(0,0xFF)
           >>> matrix.turnOffLED(5,0)
           >>> matrix.clear() #doctest: +SKIP
        '''
        self.alterSingleLED(x,y,"andnot")
    
    def toggleLED(self,x,y):
        '''
           Toggle off/on single LED at x,y
           - x = Column (0..7)
           - y = Row (0..7)
           
           Example:
           >>> matrix = EightByEight().setUp()
           >>> matrix.setRow(0,0xFF) #doctest: +SKIP
           >>> matrix.toggleLED(7,0)
           >>> matrix.toggleLED(6,0)
           >>> matrix.toggleLED(5,0)
           >>> matrix.toggleLED(6,0)
           >>> matrix.toggleLED(7,0)
           >>> matrix.clear() #doctest: +SKIP
        '''
        return self.alterSingleLED(x,y,"xor")
    

if __name__ == "__main__":
    import doctest
    doctest.testmod()
