import RPi.GPIO as GPIO
import smbus
import time

# Timing constants
# These are seemingly unnecessary and just slow everything down
# Uncomment the time.sleep() calls below if you're having problems
_E_PULSE = 0.00005
_E_DELAY = 0.00005

class GPIO4Bit:
    def __init__(self, disp_rs, disp_e, disp_d):
        GPIO.setup(disp_e, GPIO.OUT)
        GPIO.setup(disp_rs, GPIO.OUT)

        for pin in disp_d:
            GPIO.setup(pin, GPIO.OUT)

        self._disp_rs = disp_rs
        self._disp_e = disp_e
        self._disp_d = disp_d

    def send_byte(self, bits, mode):
        GPIO.output(self._disp_rs, mode)

        def pulse():
            # Toggle 'Enable' pin
            #time.sleep(_E_DELAY)    
            GPIO.output(self._disp_e, True)  
            #time.sleep(_E_PULSE)
            GPIO.output(self._disp_e, False)  
            #time.sleep(_E_DELAY)      

        for idx, pin in enumerate(self._disp_d):
            GPIO.output(pin, bool(bits & (1 << (idx + 4))))

        pulse()

        for idx, pin in enumerate(self._disp_d):
            GPIO.output(pin, bool(bits & (1 << idx)))

        pulse()
    
class GPIO8Bit:
    def __init__(self, disp_rs, disp_e, disp_d):
        GPIO.setup(disp_e, GPIO.OUT)
        GPIO.setup(disp_rs, GPIO.OUT)

        for pin in disp_d:
            GPIO.setup(pin, GPIO.OUT)

        self._disp_rs = disp_rs
        self._disp_e = disp_e
        self._disp_d = disp_d

    def send_byte(self, bits, mode):
        GPIO.output(self._disp_rs, mode)

        for idx, pin in enumerate(self._disp_d):
            GPIO.output(pin, bool(bits & (1 << (idx + 4))))

        #time.sleep(_E_DELAY)    
        GPIO.output(self._disp_e, True)  
        #time.sleep(_E_PULSE)
        GPIO.output(self._disp_e, False)  
        #time.sleep(_E_DELAY)      


class GPIO74HC595:
    def __init__(self, disp_rs, disp_e, shift_data, shift_clock, shift_latch):
        GPIO.setup(disp_e, GPIO.OUT)
        GPIO.setup(disp_rs, GPIO.OUT)
        GPIO.setup(shift_data, GPIO.OUT)
        GPIO.setup(shift_clock, GPIO.OUT)
        GPIO.setup(shift_latch, GPIO.OUT)

        self._disp_rs = disp_rs
        self._disp_e = disp_e
        self._shift_data = shift_data
        self._shift_clock = shift_clock
        self._shift_latch = shift_latch

    def send_byte(self, bits, mode):
        GPIO.output(self._disp_rs, mode)

        GPIO.output(self._shift_latch, False)
        for i in range(7, -1, -1):
            GPIO.output(self._shift_clock, False)
            bit = (((1 << i) & bits) != 0)
            GPIO.output(self._shift_data, bit)
            GPIO.output(self._shift_clock, True)
        GPIO.output(self._shift_latch, True)

        #time.sleep(_E_DELAY)    
        GPIO.output(self._disp_e, True)  
        #time.sleep(_E_PULSE)
        GPIO.output(self._disp_e, False)  
        #time.sleep(_E_DELAY)      

I2C_DEVICE = 0x20
I2C_IODIRA = 0x00
I2C_IODIRB = 0x01
I2C_GPIOA = 0x12
I2C_GPIOB = 0x13
I2C_OLATA = 0x14
I2C_OLATB = 0x15
I2C_GPUUA = 0x0c
I2C_GPUUB = 0x0d

class MCP23017:
    def __init__(self):
        self._bus = smbus.SMBus(1)
        self._bus.write_byte_data(I2C_DEVICE, I2C_IODIRA, 0x00)
        self._bus.write_byte_data(I2C_DEVICE, I2C_IODIRB, 0xfc)

        self._bus.write_byte_data(I2C_DEVICE, I2C_GPUUB, 0xfc)

    def send_byte(self, byte, t):
        ibyte = ((byte >> 7) & 1) | \
                (((byte >> 6) & 1) << 1) | \
                (((byte >> 5) & 1) << 2) | \
                (((byte >> 4) & 1) << 3) | \
                (((byte >> 3) & 1) << 4) | \
                (((byte >> 2) & 1) << 5) | \
                (((byte >> 1) & 1) << 6) | \
                (((byte & 1) << 7))
        if t:
            self.write_chr(ibyte)
        else:
            self.write_cmd(ibyte)

    def write_chr(self, byte):
        self._bus.write_byte_data(I2C_DEVICE, I2C_OLATA, byte)
        self._bus.write_byte_data(I2C_DEVICE, I2C_OLATB, 0x3)
        self._bus.write_byte_data(I2C_DEVICE, I2C_OLATA, byte)
        self._bus.write_byte_data(I2C_DEVICE, I2C_OLATB, 0x2)

    def write_cmd(self, byte):
        self._bus.write_byte_data(I2C_DEVICE, I2C_OLATA, byte)
        self._bus.write_byte_data(I2C_DEVICE, I2C_OLATB, 0x1)
        self._bus.write_byte_data(I2C_DEVICE, I2C_OLATA, byte)
        self._bus.write_byte_data(I2C_DEVICE, I2C_OLATB, 0x0)
