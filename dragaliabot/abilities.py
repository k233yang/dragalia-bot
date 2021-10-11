from bs4 import BeautifulSoup


class Abilities:
    def __init__(self, soupResults):
        self.abilityDescription = self.getAbilityDescription(soupResults)
        self.abilityName = self.getAbilityName(soupResults)

    def getAbilityDescription(self, soupResults):
        abilities = []
        ability = soupResults.find_all("div", class_ = "ability-table")
        for i in range(len(ability)):
            # para = ability[i].find("p")
            # abilities.append(para.get_text().strip())
            print(ability[i].get_text().strip())
        return abilities
    def getAbilityName(self, soupResults):
        names = []
        ability = soupResults.find_all("div", class_ = "ability-header")
        for i in range(len(ability)):
            if (i != len(ability)-1) and (ability[i+1].get_text().strip() != ability[i].get_text().strip()):
                names.append(ability[i].get_text().strip())
            elif i == len(ability)-1:
                names.append(ability[i].get_text().strip())
        return names