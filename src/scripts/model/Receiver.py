class Receiver:

    # class attribute
    name = ""
    action = ""
    hasAction = False

    # instance attribute
    def __init__(self, name,action,hasAction):
        self.name = name
        self.action = action
        self.hasAction = hasAction

