#!/usr/bin/python

import sys
import time
import smbus

bus = smbus.SMBus(1)

DEVICE = 0x20
IODIRA = 0x00
IODIRB = 0x01
GPIOA = 0x12
GPIOB = 0x13
OLATA = 0x14
OLATB = 0x15
GPUUA = 0x0c
GPUUB = 0x0d

DISP_CHR = True
DISP_CMD = False

DISP_LINE_1 = 0x80 # LCD RAM address for the 1st line.
DISP_LINE_2 = 0xC0 # LCD RAM address for the 2nd line.

# Extension register SD, see datasheet.
SD_ENABLE = 0x79
SD_DISABLE = 0x78

# Extension register RE, see datasheet.
# Blink and reverse display is also encoded in here, but we're not using it.
RE_ENABLE = 0x2A
RE_DISABLE = 0x28

# Needs SD and RE unset.
# Also encodes cursor and blink, but we're not using them.
DISP_ON = 0x0C
DISP_OFF = 0x08

# Needs SD unset.
DISP_CLEAR = 0x01


def send(byte, t):
    ibyte = ((byte >> 7) & 1) | \
            (((byte >> 6) & 1) << 1) | \
            (((byte >> 5) & 1) << 2) | \
            (((byte >> 4) & 1) << 3) | \
            (((byte >> 3) & 1) << 4) | \
            (((byte >> 2) & 1) << 5) | \
            (((byte >> 1) & 1) << 6) | \
            (((byte & 1) << 7))
    if t:
        write_chr(ibyte)
    else:
        write_cmd(ibyte)

def write_chr(byte):
    bus.write_byte_data(DEVICE, OLATA, byte)
    bus.write_byte_data(DEVICE, OLATB, 0x3)
    bus.write_byte_data(DEVICE, OLATA, byte)
    bus.write_byte_data(DEVICE, OLATB, 0x2)

def write_cmd(byte):
    bus.write_byte_data(DEVICE, OLATA, byte)
    bus.write_byte_data(DEVICE, OLATB, 0x1)
    bus.write_byte_data(DEVICE, OLATA, byte)
    bus.write_byte_data(DEVICE, OLATB, 0x0)

def main(argv):
    bus.write_byte_data(DEVICE, IODIRA, 0x00)
    bus.write_byte_data(DEVICE, IODIRB, 0xfc)
    bus.write_byte_data(DEVICE, GPUUB, 0xfc)

    # Enable Internal Regulator
    send(RE_ENABLE, DISP_CMD)
    send(0x08, DISP_CMD)
    send(0x71, DISP_CMD)
    send(0x5C, DISP_CHR)
    send(RE_DISABLE, DISP_CMD)

    # Set Display Off
    send(DISP_OFF, DISP_CMD)

    # Set Display Clock Divide Ratio and Oscillator Frequency
    send(RE_ENABLE, DISP_CMD)
    send(SD_ENABLE, DISP_CMD)
    send(0xD5, DISP_CMD)
    send(0x70, DISP_CMD)
    send(SD_DISABLE, DISP_CMD)

    # Set Display Mode
    send(0x08, DISP_CMD)

    # Set Re-Map
    send(0x06, DISP_CMD)

    # CGROM/CGRAM Management
    send(0x72, DISP_CMD)
    send(0x00, DISP_CHR)

    # Set OLED Characterization
    send(SD_ENABLE, DISP_CMD)

    # Set SEG Pins Hardware Configuration
    send(0xDA, DISP_CMD)
    send(0x10, DISP_CMD)

    # Set Segment Low Voltage & GPIO
    send(0xDC, DISP_CMD)

    send(0x03, DISP_CMD)

    # Recommended 100ms delay
    time.sleep(0.1)

    # Set Contrast Control
    # This doesn't seem to do anything for me.
    # But you can use hardware contrast control instead.
    send(0x81, DISP_CMD)
    send(0xFF, DISP_CMD)

    # Set Pre-Charge Period
    send(0xD9, DISP_CMD)
    send(0xF1, DISP_CMD)

    # Set VCOMH Deselect Level
    send(0xDB, DISP_CMD)
    send(0x40, DISP_CMD)

    # Exiting Set OLED Characterization
    send(SD_DISABLE, DISP_CMD)
    send(RE_DISABLE, DISP_CMD)

    # Set Display Off
    send(DISP_OFF, DISP_CMD)

    # Clear Display
    send(DISP_CLEAR, DISP_CMD)

    # Set DDRAM Address
    send(0x80, DISP_CMD)

    # Set Display On
    send(DISP_ON, DISP_CMD)

    send(DISP_LINE_1, DISP_CMD)
    text = 'ABCDEFGHIJKLMNOP'
    for mchar in text:
        send(ord(mchar), DISP_CHR)

    while True:
        time.sleep(0.5)
        send(DISP_LINE_2, DISP_CMD)

        state = bus.read_byte_data(DEVICE, GPIOB)
        text = '=> ' + str(state)

        for mchar in text:
            send(ord(mchar), DISP_CHR)


    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
