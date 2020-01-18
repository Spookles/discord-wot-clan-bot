import requests
import json
from tank import Tank

class Player:
    id = 0
    name = ""
    tankCount = 0
    tanks = []
    newMarks = []
    firstLoop = True

    def __init__(self, _id, _name, _tanks):
        #all tanks of player: https://api.worldoftanks.eu/wot/account/tanks/?application_id=0ecfda2435a084d16fa9e02ea75ee0db&account_id=502253961&fields=tank_id
        #tank achievments by tank id: https://api.worldoftanks.eu/wot/tanks/achievements/?application_id=1119ac87433be4957549e3f3e83e18d4&account_id=502253961&fields=achievements%2C+tank_id
        self.id = _id
        self.name = _name
        self.tanks = _tanks
        self.newMarks = [0] * 100

        self.retrieveTanks()
        print("Retrieved all tanks!")

    def retrieveTanks(self):
        api_url = "https://api.worldoftanks.eu/wot/tanks/achievements/?application_id=1119ac87433be4957549e3f3e83e18d4&account_id={}&fields=achievements%2C+tank_id".format(self.id)
        response = requests.get(api_url)
        jsonResponse = response.json()['data'][str(self.id)]

        loopCount = 0
        if not response.json()['data'][str(self.id)] == None:
            for tank in jsonResponse:
                for tankDB in self.tanks:
                    if tank['tank_id'] == tankDB.id:
                        try:
                            tankDB.setPreviousMark(tankDB.getMark())
                            tankDB.setMark(int(tank['achievements']['marksOnGun']))
                            if self.firstLoop != True:
                                tankDB.setMark(4)
                                if tankDB.getMark() != tankDB.getPreviousMark():
                                    self.newMarks[loopCount] = tankDB
                                    loopCount+=1
                        except:
                            False
        self.firstLoop = False
