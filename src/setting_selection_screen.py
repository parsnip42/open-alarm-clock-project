from selection_screen import SelectionScreen

class SettingSelectionScreen(SelectionScreen):
    def __init__(self, context, settings, title, key, items):
        super(SettingSelectionScreen, self).__init__(context,
                                                     title,
                                                     items,
                                                     settings[key],
                                                     self._setting_selected)
        self._settings = settings
        self._key = key
        
    def _setting_selected(self):
        self._settings[self._key] = self.selected_item

