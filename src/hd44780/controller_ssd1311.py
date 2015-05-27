import time

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

class ControllerSSD1311:
    def __init__(self, connector):
        self._connector = connector

    def start(self):
        send = self._connector.send_byte

        # Initialise display
        # Taken from Midas datasheet
        # I have no idea what half this crap does

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

    def stop(self):
        send = self._connector.send_byte

        # Power down VCC
        send(RE_ENABLE, DISP_CMD)
        send(SD_ENABLE, DISP_CMD)
        send(0xDC, DISP_CMD)
        send(0x02, DISP_CMD)
        send(SD_DISABLE, DISP_CMD)
        send(RE_DISABLE, DISP_CMD)

        # Set Display Off
        send(DISP_OFF, DISP_CMD)

    def send_line(self, line, text):
        send = self._connector.send_byte
        
        if line == 0:
            send(DISP_LINE_1, DISP_CMD)
        else:
            send(DISP_LINE_2, DISP_CMD)
        
        for mchar in text:
            send(ord(mchar), DISP_CHR)
