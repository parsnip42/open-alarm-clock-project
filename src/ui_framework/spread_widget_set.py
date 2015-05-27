from widget_container import WidgetContainer

class SpreadWidgetSet(WidgetContainer):
    def __init__(self, widgets = []):
        super(SpreadWidgetSet, self).__init__()
        self.container_set_widgets(widgets)

    def get_paint_str(self, max_width):
        contents = [widget.widget_get_paint_str(max_width) for widget in self.container_get_widgets()]
        sep = " " * max((max_width - len("".join(contents))) / (len(contents) + 1), 0)

        return sep.join(contents)
