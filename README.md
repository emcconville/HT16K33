# HT16K33 Python Library #

A simple python library to control products using the HT16K33 IC.

**Currently supported**

 + [8x8 LED Matrix](http://adafruit.com/products/872) (_HT16K33.EightByEight_)

**To Do**

 - [BiColor LED Square Pixel Matrix](http://adafruit.com/products/902) (_HT16K33.BiColor_)
 - [4 Digit 7-Segment Display](http://adafruit.com/products/878) (_HT16K33.FourDigit_)

## Dependencies

The only dependency is Python's SMBus module; which, ships with Linux's [i2c-tools][1] development tools. 
The module _SMBus_ opens a simple protocol to transport data between Linux OS and _any_ i2c integrated circuit.

If HT16K33 library is unable to load the _SMBus_ module, then this library will genereate an internal dummy object
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

Compile core (update paths and C-flags as needed)

    $ make 
    $ make install

Compile eepromer (if needed)

    $ make -C eepromer
    $ install -Dm755 eepromer/eeprog eepromer/eeprom eepromer/eepromer /usr/sbin

Build and install python2's SMBus

    $ cd py-smbus
    $ python setup.py build
    $ python setup.py install

## Usage

Connect i2c device, and identify address.

    $ i2cdetect -y 0

### EightByEight

Draw a cross from corner to corner.

```python

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

    from HT16K33 import EightByEight
    import time
    
	# Enable device
    matrix=EightByEight(bus=0,address=0x70).setUp()
	
	# Turn on all LEDS
	for row in range(0,8):
	  matrix.setRow(row,0xFF)
    
	# Adjust duty 
	for duty in range(0,16):
	  matrix.setBrightness(duty)
```

[1]:(http://dl.lm-sensors.org/i2c-tools/releases/i2c-tools-3.1.0.tar.bz2)