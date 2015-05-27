import time
from font import Font

DISP_CHR = True
DISP_CMD = False

DISP_LINE_1 = 0x80 # LCD RAM address for the 1st line
DISP_LINE_2 = 0xC0 # LCD RAM address for the 2nd line 

class ControllerGeneric:
    def __init__(self, connector):
        self._connector = connector

    def start(self):
        send = self._connector.send_byte

        send(0x33, DISP_CMD) # ??
        send(0x32, DISP_CMD) # ??
        send(0x28, DISP_CMD) # 4-bit, 2-line interface

        send(0x0C, DISP_CMD) # Hide cursor
        send(0x06, DISP_CMD) # Display Shift OFF, Increment
        send(0x02, DISP_CMD) # Reset Cursor
        send(0x17, DISP_CMD) # Display on, character mode
        send(0x01, DISP_CMD) # Clear Display
        
        self.setup_font(1, Font.FOCUS_LEFT)
        self.setup_font(2, Font.FOCUS_RIGHT)
        self.setup_font(3, Font.ALARM_INDICATOR)

    def stop(self):
        send = self._connector.send_byte

        send(0x01, DISP_CMD) # Clear Display
        send(0x02, DISP_CMD) # Reset Cursor
        send(0x08, DISP_CMD) # Power Off Display

    def send_line(self, line, text):
        send = self._connector.send_byte

        if line == 0:
            send(DISP_LINE_1, DISP_CMD)
        else:
            send(DISP_LINE_2, DISP_CMD)

        for mchar in text:
            send(ord(mchar), DISP_CHR)

    def setup_font(self, char, char_data):
        send = self._connector.send_byte

        send(0x40 + (char << 3), DISP_CMD)
        for x in Font.bit_array(char_data):
            send(x, DISP_CHR)






