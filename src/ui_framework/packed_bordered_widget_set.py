from label_widget import LabelWidget
from widget_container import WidgetContainer

class PackedBorderedWidgetSet(WidgetContainer):
    def __init__(self,  left = None, center = None, right = None):
        super(PackedBorderedWidgetSet, self).__init__()
        self.left = left or LabelWidget()
        self.center = center or LabelWidget()
        self.right = right or LabelWidget()
        self.container_set_widgets([self.left, self.center, self.right])

    def get_paint_str(self, max_width):
        left_str = self.left.widget_get_paint_str(max_width / 2)
        right_str = self.right.widget_get_paint_str(max_width / 2)
        center_str = self.center.widget_get_paint_str(max_width - (len(left_str) + len(right_str)))

        return left_str + center_str + right_str




















