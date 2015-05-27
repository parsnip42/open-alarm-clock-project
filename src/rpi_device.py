from hd44780 import HD44780Display
from ui_common import Event
import thread
import time

#import RPi.GPIO as GPIO

class RPiDevice:
    # Change as appropriate if necessary.
    # Note that GPIO pin 27 is 21 on the RPi revision 1.
    _BUTTON_PINS = [ 4, 27, 17, 22 ]

    def __init__(self):
        #GPIO.setmode(GPIO.BCM) # Use BCM GPIO numbers

        self.display = HD44780Display()
        self._stop = False

    def start(self, event_manager):
        self._event_manager = event_manager

        #for pin in self._BUTTON_PINS:
            # Configured for internal pull up resistors
            # Use this if your GPIO buttons are connected to
            # GND when pressed.
        #    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.display.start()

        def push_event(event, event_args):
            event_manager.post_event(event, event_args)

        #def create_button_callback(button):
        # return lambda channel: push_event(Event.BUTTON_UP if GPIO.input(channel) else Event.BUTTON_DOWN, button)

        #for i in range(0, len(self._BUTTON_PINS)):
        #    GPIO.add_event_detect(self._BUTTON_PINS[i], GPIO.BOTH, callback=create_button_callback(i))

        def poll_i2c():
            last_mask = 0

            while True:
                time.sleep(0.01)
                mask = self.display._connector._bus.read_byte_data(0x20, 0x13)
                mask = ((mask >> 2) & 0xf) ^ 0xf
                diff = last_mask ^ mask
                last_mask = mask

                button = 0
                while diff:
                    if diff & 1:
                        print button, (mask >> button) & 1
                        push_event(Event.BUTTON_DOWN if (mask >> button) & 1 else Event.BUTTON_UP, button)
                    button += 1
                    diff >>= 1
                

        thread.start_new_thread(poll_i2c, ())
        event_manager.start()

        self.display.stop()

        #for pin in self._BUTTON_PINS:
            #GPIO.remove_event_detect(pin)

        #GPIO.cleanup()

    def stop(self):
        self._event_manager.stop()
