from widget import Widget

class ButtonWidget(Widget):
    def __init__(self, text):
        super(ButtonWidget, self).__init__()
        self.text = text

    def get_paint_str(self, max_width):
        return self.text
