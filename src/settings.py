import json
from common import CommonJSONEncoder
from common import CommonJSONDecoder

class Settings(object):
    class Entry(object):
        def __init__(self,
                     key,
                     value_type,
                     value,
                     multi = False,
                     ui_name = "",
                     ui_options = None):

            self.key = key
            self.value_type = value_type
            self.multi = multi
            self.ui_name = ui_name
            self.ui_options = ui_options

            self.value = value

        @property
        def value(self):
            return self._value

        @value.setter
        def value(self, value):
            if not self.multi:
                self._value = self._cast(value)
            else:
                if not isinstance(value, list):
                    self._value = [self._cast(value)]
                else:
                    self._value = [self._cast(item) for item in value]

        def _cast(self, value):
            if not isinstance(value, self.value_type):
                return self.value_type(value)
            else:
                return value

    def __init__(self, cfg_file):
        self._cfg_file = cfg_file
        self._data = {}

    def load(self):
        try:
            with open(self._cfg_file, "r") as file_handle:
                for key, value in json.load(file_handle, cls=CommonJSONDecoder).items():
                    try:
                        self[key] = value
                    except ValueError as ve:
                        print "WARNING: " + ve.message
        except ValueError as ve:
            print "WARNING: Failed to load settings from " + self._cfg_file
            print ve.message
        except IOError:
            print "WARNING: Could not open '" + self._cfg_file + "' to load settings"

    def save(self):
        items = {}
        for key, entry in self._data.iteritems():
            items[key] = entry.value

        try:
            with open(self._cfg_file, "w") as file_handle:
                json.dump(items, file_handle, cls=CommonJSONEncoder, indent=4)
        except IOError:
            print "WARNING: Could not open '" + self._cfg_file + "' to save settings"

    def define(self, entry):
        self._data[entry.key] = entry

    def get_entry(self, key):
        if key in self._data:
            return self._data[key]

        return None

    def __getitem__(self, key):
        if key in self._data:
            return self._data[key].value

        return None

    def __setitem__(self, key, value):
        if key in self._data:
            self._data[key].value = value
            self.save()
