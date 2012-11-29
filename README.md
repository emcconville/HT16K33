# HT16K33 Python Library #

A simple python library to control products using the HT16K33 IC.

** Currently supported **

 - 8x8 LED matrix

** To Do **

## Dependencies

Python's SMBus shared object (ships with i2c-tools). 

#### Debain
Install i2c-tools, and SMBus

    $ sudo apt-get install i2c-tools python-smbus

#### Arch

    $ pacman -S i2c-tools

#### Source

    # Download source & extract
    $ curl -O http://dl.lm-sensors.org/i2c-tools/releases/i2c-tools-3.1.0.tar.bz2
    $ tar jxvf i2c-tools-3.1.0.tar.bz2 && cd i2c-tools-3.1.0
    # Compile core (update paths and C-flags as needed)
    $ make 
    $ make install
    # Compile eepromer (if needed)
    $ make -C eepromer
    $ install -Dm755 eepromer/eeprog eepromer/eeprom eepromer/eepromer /usr/sbin
    # Build and install python2's SMBus
    $ cd py-smbus
    $ python setup.py build
    $ python setup.py install

## Usage

Connect i2c device, and identify bus + address.

    $ BUS=0
    $ i2cdetect -y $BUS

### EightByEight

    #!/bin/env python
    from HT16K33 import EightByEight
    import time
    bus=0
    address=0x70
    matrix=EightByEight(bus,address).setUp()
    for i in range(0,8):
      matrix.turnOnLED(i,i)
      matrix.turnOnLED(8-i,i)
      time.sleep(0.25)
