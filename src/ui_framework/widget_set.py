from widget_container import WidgetContainer

class WidgetSet(WidgetContainer):
    def __init__(self, widgets = []):
        super(WidgetSet, self).__init__()
        self.container_set_widgets(widgets)

    def get_paint_str(self, max_width):
        return "".join([widget.widget_get_paint_str(max_width)
                        for widget in self.container_get_widgets()])
















