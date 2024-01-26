from keys import keys

class Action:
    pass

class EscapeAction(Action):
    pass

class Enter(Action):
    pass

class Backspace(Action):
    pass

class Arrow(Action):
    def __init__(self, key):
        self.key = key
        self.direction = keys.arrows[self.key]

class InpToggle(Action):
    pass

class InpAdd(Action):
    def __init__(self, key):
        super().__init__() # wtf

        self.key = key
        self.char = keys.keyStr[self.key]

class RollDie(Action):
    def __init__(self, key):
        super().__init__() # wtf

        self.key = key
        self.num = keys.numKeys[self.key]
