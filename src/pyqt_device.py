from ui_common import Event

import sys
import time
from threading import Thread
from PyQt4 import QtGui, QtCore

class _PyQtDisplay(QtGui.QWidget):
    def __init__(self):
        super(_PyQtDisplay, self).__init__()

        self._lines = []

        line = QtGui.QLabel("", self)
        line.move(0, 0)
        line.resize(300, 20)
        self._lines.append(line)

        line = QtGui.QLabel("", self)
        line.move(0, 20)
        line.resize(300, 20)
        self._lines.append(line)
        
        button_text = ["O", "X", "<-", "->"]
        for i in range(0, 4):
            button = QtGui.QPushButton(button_text[i], self)
            
            def fire_func(n):
                return lambda: self.fire_button(n)

            button.clicked.connect(fire_func(i))
            button.resize(button.sizeHint())
            button.move(50 * i, 50)       
            button.resize(50, 25)

        self.setGeometry(300, 300, 200, 75)
        self.setWindowTitle("OAC")    
        self.show()
    
    def text(self, text, line):
        self._set_line(line, text)

    def width(self, line):
        return 16

    def _set_line(self, line, text):
        self._lines[line].setText(text[0:16])

    def fire_button(self, button):
        self.event_manager.post_event(Event.BUTTON_DOWN, button)
        self.event_manager.post_event(Event.BUTTON_UP, button)
        

class PyQtDevice:
    def __init__(self):
        self._app = QtGui.QApplication(sys.argv)
        self.display = _PyQtDisplay()

    def start(self, event_manager):
        self.display.event_manager = event_manager

        def event_manager_start():
            event_manager.start()

        thread = Thread(target=event_manager_start)
        thread.start()
        sys.exit(self._app.exec_())

    def stop(self):
        sys.exit(0)
