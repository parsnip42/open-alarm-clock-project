from ui_framework import LabelWidget
from ui_framework import AnimatedChoiceWidget
from ui_framework import PackedBorderedWidgetSet
from entry_screen import EntryScreen

class MenuScreen(EntryScreen):
    def __init__(self, context, title, items):
        self._title = title
        self._items = items
        super(MenuScreen, self).__init__(context)

    def init_layout(self, canvas):
        self._title_label = canvas.set_widget(LabelWidget(self._title), 0)
        self._choice_widget = AnimatedChoiceWidget(self._items)
        
        label_left = LabelWidget(chr(2))
        label_right = LabelWidget(chr(1))

        widget_set = PackedBorderedWidgetSet(label_left, self._choice_widget, label_right)
        canvas.set_widget(widget_set, 1)
        
    def apply_changes(self, stack):
        select_func = self._choice_widget.selected_item
        if select_func != None:
            select_func()
