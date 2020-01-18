class Tank:
    def __init__(self, _id, _name):
        self.id = _id
        self.name = _name
        self.mark = 0
        self.previousMark = 0

    def setMark(self, _mark):
        self.mark = _mark

    def getMark(self):
        return self.mark

    def setPreviousMark(self, _mark):
        self.previousMark = _mark

    def getPreviousMark(self):
        return self.previousMark

    def getName(self):
        return self.name
