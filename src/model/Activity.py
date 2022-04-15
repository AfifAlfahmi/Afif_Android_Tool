class Activity:

    # class attribute
    name = ""
    hasMain = False

    # instance attribute
    def __init__(self, name, hasMain):
        self.name = name
        self.hasMain = hasMain
