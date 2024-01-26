import math

class character():
    def __init__(self, hpMax, mpMax, cclass, atk, invSize):
        self.hpMax = hpMax
        self.hp = math.floor(self.hpMax * .8)
        self.mpMax = mpMax
        self.mp = self.mpMax
        self.cclass = cclass
        self.atk = atk
        self.invSize = invSize # 10
        self.inv = [{"name": str(i) + " index"} if i < 15 else None for i in range(invSize)]
        self.hotbar = [{} for i in range(5)]
        self.exp = 0
        self.lvlup = 20
        self.lvl = 0

        self.posx = 50
        self.posy = 50
        self.posArea = "tutorial"

        self.quests = {
            "completed": [],
            "available": [
                {"name": "filler 1 asdfasdfsadf", "desc": "filler", "id": "quests:intro:one"},
                {"name": "filler 2 asdfasdfsadf", "desc": "filler", "id": "quests:intro:one"},
                {"name": "filler 3 asdfasdfsadf", "desc": "filler", "id": "quests:intro:one"},
                {"name": "filler 4 asdfasdfsadf", "desc": "filler", "id": "quests:intro:one"},
                {"name": "filler 5 asdfasdfsadf", "desc": "filler", "id": "quests:intro:one"},
                {"name": "filler 6 asdfasdfsadf", "desc": "filler", "id": "quests:intro:one"},
            ]
        }
    
    def invMove(self, i, j):
        self.inv[i], self.inv[j] = self.inv[j], self.inv[i]
    
    def invCheckEmpty(self):
        if None in self.inv:
            return True
        return False
    
    def invAddItem(self, item):
        for i in range(len(self.inv)):
            if self.inv[i] is None:
                self.inv[i] = item
                return True
        return False
