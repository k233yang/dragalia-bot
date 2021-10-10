from bs4 import BeautifulSoup

class Stats:
    def __init__(self, soupResults, soupResults2):
        self.hp = self.getHp(soupResults)
        self.str = self.getStr(soupResults)
        self.element = self.getElement(soupResults2)
        self.weapon = self.getWeapon(soupResults2)

    def getHp(self, soupResults):
        return soupResults.find(id='adv-hp').text
        #print(HP.text)
    
    def getStr(self, soupResults):
        return soupResults.find(id='adv-str').text
        #print(Str.text)
    
    def getElement(self, soupResults2):
        for line in soupResults2:
            if "Element" in line['alt']:
                return line['alt'].split(" ")[2][:-4]
        
    def getWeapon(self, soupResults2):
        for line in soupResults2:
            if "Weapon" in line['alt']:
                return line['alt'].split(" ")[2][:-4]
