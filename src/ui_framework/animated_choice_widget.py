from choice_widget import ChoiceWidget
from widget import Widget

class AnimatedChoiceWidget(Widget):
    def __init__(self, items, selected = 0):
        super(AnimatedChoiceWidget, self).__init__(highlight_focus=False)
        self._choice_widget = ChoiceWidget(items, selected)
        self._vis_selected = selected
        self._paint_position = 0
        self.direction = 0

    def prev(self):
        self._choice_widget.prev_repeat()
        if self.direction == 0:
            self._update_direction()
        return True

    def next(self):
        self._choice_widget.next_repeat()
        if self.direction == 0:
            self._update_direction()
        return True

    @property
    def selected_item(self):
        return self._choice_widget.selected_item

    def polling(self):
        return self.direction != 0

    def poll(self):
        self._update(1)

    def get_paint_str(self, max_width):
        items = self._choice_widget.items
        selected = self._choice_widget.selected_index
        item_count = len(self._choice_widget.items)
        
        pos = int(self._paint_position)
        vis_sel = self._vis_selected

        def rot_index(n):
            return n % item_count

        if self.direction == 1:
            return (items[vis_sel][0].center(max_width, " ")[pos:] +
                    items[rot_index(vis_sel + 1)][0].center(max_width, " "))
        elif self.direction == -1:
            return (items[rot_index(vis_sel - 1)][0].center(max_width, " ")[max_width - pos:] +
                    items[vis_sel][0].center(max_width, " "))
        else:
            return items[selected][0].center(max_width, " ")

    def _update_direction(self):
        selected = self._choice_widget.selected_index
        item_count = len(self._choice_widget.items)
        vis_selected = self._vis_selected

        if selected == vis_selected:
            self.direction = 0
        elif bool(selected > vis_selected) != bool(abs(vis_selected - selected) > (item_count / 2)):
            self.direction = 1
        else:
            self.direction = -1
        
    def _update(self, upd_time):
        item_count = len(self._choice_widget.items)

        def rot_index(n):
            return n % item_count

        if self.direction == 1:
            if self._paint_position > 16:
                self._paint_position = 0
                self._vis_selected = rot_index(self._vis_selected + 1)
            else:
                self._paint_position += upd_time
        elif self.direction == -1:
            if self._paint_position > 16:
                self._paint_position = 0
                self._vis_selected = rot_index(self._vis_selected - 1)
            else:
                self._paint_position += upd_time
        
        selected = self._choice_widget.selected_index
        vis_selected = self._vis_selected

        if selected == vis_selected:
            self.direction = 0
            return False
        else:
            return True
