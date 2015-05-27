from widget_container import WidgetContainer

class SingleWidgetContainer(WidgetContainer):
    def __init__(self, widget = None):
        super(SingleWidgetContainer, self).__init__()
        self.set_widget(widget)

    def get_widget(self):
        return self._widget

    def set_widget(self, widget):
        self._widget = widget
        self.container_set_widgets([widget] if widget != None else [])

    def clear(self):
        self._widget = None
        
    def get_paint_str(self, max_width):
        widget = self._widget
        return (widget.get_paint_str(max_width) if widget != None else "")


