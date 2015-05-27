from ui_framework import LabelWidget
from ui_framework import ChoiceWidget
from entry_screen import EntryScreen

class SelectionScreen(EntryScreen):
    def __init__(self, context, title, items, selected_item, select_func):
        self._title = title
        self._items = items
        self._select_func = select_func
        super(SelectionScreen, self).__init__(context)
        
        self.selected_item = selected_item

    def init_layout(self, canvas):
        self._title_label = canvas.set_widget(LabelWidget(self._title), 0)
        self._choice_widget = canvas.set_widget(ChoiceWidget(self._items), 1)
        
    def apply_changes(self, stack):
        if self._select_func != None:
            self._select_func()
        stack.pop()

    @property
    def selected_item(self):
        return self._choice_widget.selected_item

    @selected_item.setter
    def selected_item(self, value):
        self._choice_widget.selected_item = value





