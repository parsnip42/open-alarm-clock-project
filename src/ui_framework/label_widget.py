from widget import Widget

class LabelWidget(Widget):
    def __init__(self, text = ""):
        super(LabelWidget, self).__init__(can_focus=False)
        self.text = text

    def get_paint_str(self, max_width):
        return self.text
