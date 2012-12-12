# HT16K33 Python Library #

A simple python library to control products using the HT16K33 IC.

 + Adafruit's LED backpacks
   + [BiColor LED Square Pixel Matrix](http://adafruit.com/products/902) - [HT16K33.BiColor](#bicolor-square)
   + [8x8 LED Matrix](http://adafruit.com/products/872) - [HT16K33.EightByEight](#eightbyeight)
   + [4 Digit 7-Segment Display](http://adafruit.com/products/878) - [HT16K33.FourDigit](#fourdigit)

## Dependencies

The only dependency is Python's SMBus module; which, ships with Linux's [i2c-tools][1] development tools. 
The module _SMBus_ opens a simple protocol to transport data between Linux OS and _any_ i2c integrated circuit.

If HT16K33 library is unable to load the _SMBus_ module, then this library will genereate an internal dummy object.
Said dummy object will emulate **I/O** protocol, and dump actions/commands to **STDOUT**.

### Debain

_SMBus_ is isolated in a seprate package on Debain/Ubuntu. Be sure _python-smbus_ is installed

    $ sudo apt-get install i2c-tools python-smbus

### Arch

Arch's _PKGBUILD_ will include _SMBus_ with the parent i2c-tools

    $ pacman -S i2c-tools

### Source

Download source & extract

    $ curl -O http://dl.lm-sensors.org/i2c-tools/releases/i2c-tools-3.1.0.tar.bz2
    $ tar jxvf i2c-tools-3.1.0.tar.bz2 && cd i2c-tools-3.1.0

Compile core _update paths and C-flags as needed_

    $ make 
    $ make install

Compile eepromer _if needed_

    $ make -C eepromer
    $ install -Dm755 eepromer/eeprog eepromer/eeprom eepromer/eepromer /usr/sbin

Build and install python2's SMBus

    $ cd py-smbus
    $ python setup.py build
    $ python setup.py install

## Usage

Connect i2c device, and identify address.

    $ i2cdetect -y 0
         0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f                             
    00:          -- -- -- -- -- -- -- -- -- -- -- -- --                             
    10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --                             
    20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --                             
    30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --                             
    40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --                             
    50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --                             
    60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --                             
    70: 70 -- -- -- -- -- -- --  
    
### Base Object ###

Parent object inhertied by all HT16K33 LED backpacks. Not inteded for direct use.

#### Methods ####

    class Base(__builtin__.object)
     |  Methods defined here:
     |  
     |  __init__(self, **kwargs)
     |  
     |  clear(self)
     |      Loop through all data addresses, and clear any LEDS
     |  
     |  setBrightness(self, brightness=15)
     |      Set brightness level
     |      - brightness (0..15)
     |      --  0 =  1/16 duty
     |      --  1 =  2/16 duty
     |      --  2 =  3/16 duty
     |      --  3 =  4/16 duty
     |      --  4 =  5/16 duty
     |      --  5 =  6/16 duty
     |      --  6 =  7/16 duty
     |      --  7 =  8/16 duty
     |      --  8 =  9/16 duty
     |      --  9 = 10/16 duty
     |      -- 10 = 11/16 duty
     |      -- 11 = 12/16 duty
     |      -- 12 = 13/16 duty
     |      -- 13 = 14/16 duty
     |      -- 14 = 15/16 duty
     |      -- 15 = 16/16 duty
     |  
     |  setDisplay(self, on=True, blink_rate=0)
     |      Set display options
     |      - on (Boolean)
     |      - blink_rate (0..3)
     |      -- 0 = Blink off
     |      -- 1 = 2HZ
     |      -- 2 = 1HZ
     |      -- 3 = 0.5HZ
     |  
     |  setUp(self)
     |      Clear & set default state of HT16K33 internal systems
     |        
     |      - Blink disabled
     |      - Brightness 8/16 duty (half-dim)
     |      - All LEDS off
     |  
     |  turnOffOscillator(self)
     |      Disable HT16K33 internal system oscillator
     |  
     |  turnOnOscillator(self)
     |      Enable HT16K33 internal system oscillator
     |        

### EightByEight ###

#### Examples ####

```python

    #!/bin/env python
    # Draw a cross from corner to corner.
    
    from HT16K33 import EightByEight
    import time
    
    matrix=EightByEight(bus=0,address=0x70).setUp()
    for i in range(0,8):
      matrix.turnOnLED(i,i)
      matrix.turnOnLED(7-i,i)
      time.sleep(0.25)
```

```python

    #!/bin/env python
    # Cycle through all levels of brightness
    
    from HT16K33 import EightByEight
    import time
    
    # Enable device
    matrix=EightByEight(bus=0,address=0x70).setUp()
      
    # Turn on all LEDS
    for row in range(8):
      matrix.setRow(row,0xFF)
    
    # Adjust duty 
    for duty in range(16):
      matrix.setBrightness(duty)
```

#### Methods ####

    class EightByEight(_HT16K33.Base)
     |  
     |  Method resolution order:
     |      EightByEight
     |      _HT16K33.Base
     |      __builtin__.object
     |  
     |  Methods defined here:
     |  
     |  alterSingleLED(self, x, y, action=None)
     |      Manipulate single lead at point (x,y)
     |      - x = Column (0..7)
     |      - y = Row (0..7)
     |      - action = ("or","xor","andnot")
     |  
     |  getRowAddressByIndex(self, row)
     |      Retrieve address of row by index. 
     |      - row (0..7)
     |  
     |  setRow(self, row=0, columns=[])
     |      Set LED status
     |      - row (0..7)
     |      - columns (mixed)
     |      -- 8 item list of booleans
     |      -- Unsigned integer
     |      --- 0..255
     |      --- 0x00..0xFF
     |      --- 0b00000000...0b11111111
     |      
     |  toggleLED(self, x, y)
     |      Toggle off/on single LED at x,y
     |      - x = Column (0..7)
     |      - y = Row (0..7)
     |  
     |  turnOffLED(self, x, y)
     |      Turn off single LED at x,y
     |      - x = Column (0..7)
     |      - y = Row (0..7)
     |      
     |  turnOnLED(self, x, y)
     |      Turn on single LED at x,y
     |      - x = Column (0..7)
     |      - y = Row (0..7)
     |      


### BiColor Square ###

#### Examples ####

```python

    #!/bin/env python
    # Cycle through red & green colors, and render 
    # yellow line across last row
    
    from HT16K33 import BiColor
    
    # Enable device
    square=BiColor(bus=0,address=0x70).setUp()
    incr=0
    
    # Alternate between green & red columns
    for column in range(8):
      isRed=bool(incr%2)
      square.setColumn(column,0xFF,isRed)
      incr+=1
    
    # Draw yellow across last row
    for x in range(7,-1,-1):
      if bool(incr%2):
        square.turnOnRedLED(x,7)
      else:
        square.turnOnGreenLED(x,7)
      incr+=1
```
 
#### Methods ####

    class BiColor(_HT16K33.Base)
     |  Method resolution order:
     |      BiColor
     |      _HT16K33.Base
     |      __builtin__.object
     |  
     |  Methods defined here:
     |  
     |  alterSingleLED(self, x, y, action, isRed=False)
     |      Manipulate single lead at point (x,y)
     |      - x = Column (0..7)
     |      - y = Row (0..7)
     |      - action = ("or","xor","andnot")
     |      - isRed = (Boolean, default=False)
     |  
     |  getColumnAddressByIndex(self, column, isRed=False)
     |      Retrieve column address based on index & color
     |      - column (0..7)
     |      - isRed (Boolean, default=False)
     |  
     |  getRowValue(self, position=0)
     |      Retrieve value of row position
     |      - position (0..7)
     |  
     |  setColumn(self, column=0, value=0, isRed=False)
     |      Assign all LEDs in a given column
     |      
     |      - column (0..7)
     |      - value (0x00..0xFF)
     |      - isRed (Boolean, default=False)
     |  
     |  toggleGreenLED(self, x, y)
     |      Toggle single green LED at x,y
     |      - x (0..7)
     |      - y (0..7)
     |  
     |  toggleRedLED(self, x, y)
     |      Toogle single red LED at x,y
     |      - x (0..7)
     |      - y (0..7)
     |  
     |  turnOffGreenLED(self, x, y)
     |      Turn off single green LED at x,y
     |      - x (0..7)
     |      - y (0..7)
     |  
     |  turnOffLED(self, x, y)
     |      Turn off both green & red LEDs at point x,y
     |      - x (0..7)
     |      - y (0..7)
     |  
     |  turnOffRedLED(self, x, y)
     |      Turn off single red LED at x,y
     |      - x (0..7)
     |      - y (0..7)
     |  
     |  turnOnGreenLED(self, x, y)
     |      Turn on single green LED at x,y
     |      - x (0..7)
     |      - y (0..7)
     |  
     |  turnOnRedLED(self, x, y)
     |      Turn on single red LED at x,y
     |      - x (0..7)
     |      - y (0..7)

### FourDigit ###

#### Example ####

```python

    #!/bin/env python
    # Create letters "a", "b", "c", & "d" across all for digits displays
    
    from HT16K33 import FourDigit
    
    # Enable device
    digit = FourDigit().setUp()
    
    # Create characters
    a = digit.TOP_BAR | digit.MIDDLE_BAR | \
        digit.BOTTOM_BAR | digit.RIGHT_TOP_BAR | \
        digit.RIGHT_BOTTOM_BAR | digit.LEFT_BOTTOM_BAR
    b = digit.MIDDLE_BAR | digit.BOTTOM_BAR | \
        digit.LEFT_TOP_BAR | digit.LEFT_BOTTOM_BAR | \
        digit.RIGHT_BOTTOM_BAR
    c = digit.MIDDLE_BAR | digit.BOTTOM_BAR | digit.LEFT_BOTTOM_BAR
    d = digit.MIDDLE_BAR | digit.BOTTOM_BAR | \
        digit.RIGHT_TOP_BAR | digit.RIGHT_BOTTOM_BAR | \
        digit.LEFT_BOTTOM_BAR
    
    # Assign custom built characters to device
    digit.setDigit(0,a)
    digit.setDigit(1,b)
    digit.setDigit(2,c)
    digit.setDigit(3,d)
```

#### Methods ####

    class FourDigit(_HT16K33.Base)
     | 
     |  Method resolution order:
     |      FourDigit
     |      _HT16K33.Base
     |      __builtin__.object
     |
     |  Methods defined here:
     |
     |  alterSingleLED(self, position=0, new_byte=0, action=None)
     |      Manipulate single LED in character position
     |      - position (0..3)
     |      - new_byte (0..0xFF)
     |      - action   ("or","xor","andnot")
     |
     |  chrToInt(self, character)
     |      Convert character to LED display integer
     |      
     |      Each available character will have the LED display
     |      integer assigned to the CHARACTER_MAP key matching
     |      character's order. Any character not present in 
     |      CHARACTER_MAP will return 0x00 (clear LED integer.)
     |      
     |      - character (see CHARACTER_MAP)
     |
     |  getDigitAddressAtPosition(self, position=0)
     |      Retrive address by position
     |      - position (0..3)
     | 
     |  readAtPosition(self, position=0)
     |      Return LED value currently in devices EEPROM
     |      - position (0..3)
     |
     |  setDigit(self, position=0, value=0)
     |      Assign LED display to digit
     |      - position
     |      - value
     |
     |  turnOffColon(self)
     |      Disable colon symbol
     |
     |  turnOffPeriodAtPosition(self, position=0)
     |      Disable period symbol at given position
     |  turnOnColon(self)
     |      Enable colon symbol
     |  
     |  turnOnPeriodAtPosition(self, position=0)
     |      Enable period symbol at given position
     |
     |  writeDigit(self, position, char=None)
     |      Write single character to a given postion
     


[1]:(http://dl.lm-sensors.org/i2c-tools/releases/i2c-tools-3.1.0.tar.bz2)