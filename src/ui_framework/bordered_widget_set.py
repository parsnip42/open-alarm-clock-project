from label_widget import LabelWidget
from widget_container import WidgetContainer

class BorderedWidgetSet(WidgetContainer):
    def __init__(self, left = None, center = None, right = None):
        super(BorderedWidgetSet, self).__init__()
        self.left = left or LabelWidget()
        self.center = center or LabelWidget()
        self.right = right or LabelWidget()
        self.container_set_widgets([self.left, self.center, self.right])

    def get_paint_str(self, max_width):
        return "".join(map(lambda l, c, r: r if r != " " else l if l != " " else c,
                           self.left.widget_get_paint_str(max_width).ljust(max_width, " "),
                           self.center.widget_get_paint_str(max_width).center(max_width, " "),
                           self.right.widget_get_paint_str(max_width).rjust(max_width, " ")))
