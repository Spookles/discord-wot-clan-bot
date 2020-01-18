class Tank:
    id = 0
    name = ""
    mark = 0
    previousMark = 0

    def __init__(self, _id, _name):
        self.id = _id
        self.name = _name

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
