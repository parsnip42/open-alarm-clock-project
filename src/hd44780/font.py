class Font:
    FOCUS_LEFT = [
        " #   ",
        " ##  ",
        " ### ",
        " ####",
        " ### ",
        " ##  ",
        " #   ",
        "     "
        ]

    FOCUS_RIGHT = [
        "   # ",
        "  ## ",
        " ### ",
        "#### ",
        " ### ",
        "  ## ",
        "   # ",
        "     "
        ]

    ALARM_INDICATOR = [
        "#    ",
        "# #  ",
        "# # #",
        "# # #",
        "# # #",
        "# #  ",
        "#    ",
        "     "
        ]

    @staticmethod
    def bit_array(char_data):
        def mask(line):
            return sum([2**index
                        for index, char in enumerate(line[::-1])
                        if char != " "])

        return [mask(line) for line in char_data]


