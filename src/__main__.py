import os
import signal
import sys
import getopt
from settings import Settings
from default_settings import DefaultSettings
from event_manager import EventManager

def create_pyqt():
    from pyqt_device import PyQtDevice
    return PyQtDevice()

def create_rpi():
    from rpi_device import RPiDevice
    return RPiDevice()

DEVICES = {
    "pyqt": create_pyqt,
    "rpi": create_rpi
}

def create_settings():
    SETTINGS_FILE = "oacp_conf.json"
    settings = Settings(SETTINGS_FILE)
    DefaultSettings.populate(settings)
    
    settings.load()
    settings.save()

    return settings

def run_interactive(device):
    def sigint_handler(signal, frame):
        device.stop()

    signal.signal(signal.SIGINT, sigint_handler)

    event_manager = EventManager(create_settings(), device)
    device.start(event_manager)

def run_daemon(device):
    import daemon

    daemon_log = open("/var/log/oacp.log", "a")
    daemon_context = daemon.DaemonContext(working_directory="/opt/oacp",
                                          files_preserve=[daemon_log],
                                          stdout=daemon_log,
                                          stderr=daemon_log)

    def sigterm_handler(signal, frame):
        device.stop()

    daemon_context.signal_map = {
        signal.SIGTERM: sigterm_handler
    }
    
    settings = create_settings()

    with daemon_context:
        event_manager = EventManager(settings, device)
        device.start(event_manager)
    
    daemon_log.close()

    # GPIO event_detect threads don't exit as daemon.
    os._exit(0)

def usage():
    print "Syntax: [-d] [device name]"

def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], "d", ["daemon"])
    except getopt.GetoptError as err:
        print err
        usage()
        return 2

    if len(args) > 2:
        usage()
        return 2

    device_name = args[0] if len(args) == 1 else "pyqt"

    if device_name in DEVICES:
        device = DEVICES[device_name]()
    else:
        print "Unknown device '" + device_name + "'."
        return 1

    if len(opts) > 0 and opts[0][0] == "-d":
        run_daemon(device)
    else:
        run_interactive(device)

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
