# HT16K33 Python Library #

A simple python library to control products using the HT16K33 IC.

**Currently supported**

 + [8x8 LED Matrix](http://adafruit.com/products/872) ( _HT16K33.EightByEight_ )
 + [BiColor LED Square Pixel Matrix](http://adafruit.com/products/902) ( _HT16K33.BiColor_ )

**To Do**

 - [4 Digit 7-Segment Display](http://adafruit.com/products/878) ( _HT16K33.FourDigit_ )

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

### EightByEight

Draw a cross from corner to corner.

```python
    #!/bin/env python
    
    from HT16K33 import EightByEight
    import time
    
    matrix=EightByEight(bus=0,address=0x70).setUp()
    for i in range(0,8):
      matrix.turnOnLED(i,i)
      matrix.turnOnLED(7-i,i)
      time.sleep(0.25)
```

Cycle through all levels of brightness.

```python
    #!/bin/env python
    
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

### BiColor Square

Cycle through all colors

```python
    #!/bin/env python
    
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

### FourColor

Display letters "a", "b", "c", & "d"

```python
    #!/bin/env python
    
    from HT16K33 import FourColor
    
    # Enable device
    digit = FourColor().setUp()
    
    # Create characters
    a = digit.TOP_BAR | digit.MIDDLE_BAR | 
        digit.BOTTOM_BAR | digit.RIGHT_TOP_BAR | 
        digit.RIGHT_BOTTOM_BAR | digit.LEFT_BOTTOM_BAR
    b = digit.MIDDLE_BAR | digit.BOTTOM_BAR |
        digit.LEFT_TOP_BAR | digit.LEFT_BOTTOM_BAR |
        digit.RIGHT_BOTTOM_BAR
    c = digit.MIDDLE_BAR | digit.BOTTOM_BAR | digit.RIGHT_BOTTOM_BAR
    d = digit.MIDDLE_BAR | digit.BOTTOM_BAR |
        digit.RIGHT_TOP_BAR | digit.RIGHT_BOTTOM_BAR
        digit.LEFT_BOTTOM_BAR
    
    # Assign custom built characters to device
    digit.setDigit(0,a)
    digit.setDigit(1,b)
    digit.setDigit(2,c)
    digit.setDigit(3,d)
```

[1]:(http://dl.lm-sensors.org/i2c-tools/releases/i2c-tools-3.1.0.tar.bz2)