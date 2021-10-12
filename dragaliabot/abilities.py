from bs4 import BeautifulSoup


class Abilities:
    def __init__(self, soupResults):
        self.abilityDescription = self.getAbilityDescription(soupResults)
        self.abilityName = self.getAbilityName(soupResults)

    def getAbilityDescription(self, soupResults):
        descriptions = []
        ability = soupResults.find_all("div", class_ = "ability-table")
        for k in range(len(ability)):
            firstSkill = ability[k].get_text().strip()
            skillParts = []
            track = 0
            j = 0
            #Adding every line separated by a newline to a list
            for i in range(len(firstSkill)):
                if firstSkill[i] == '\n':
                    skillParts.append(firstSkill[track:i])
                    track += j
                    j = 0
                elif i == len(firstSkill) -1:
                    skillParts.append(firstSkill[track:i+1])
                j+=1
            
            #Checking list for ability descriptions and hardcoding indexes
            for i in range(len(skillParts)):
                #For some reason the chain coabs has different indexing than the other abilities/coabs
                if k == 1 and (i+4)%7 == 0 and i >= 10:
                    #print(skillParts[0].lstrip()+" Lv"+str((i+4)/7 -1)[0])
                    #print(skillParts[i][1:])
                    descriptions.append(skillParts[i][1:])
                #Every 6th, 13th, 20th, etc index will have the skill description
                elif k!=1 and (i+1)%7 == 0:
                    #print(skillParts[2].lstrip()+" Lv"+str((i+1)/7)[0])
                    #print(skillParts[i][1:])
                    descriptions.append(skillParts[i][1:])
                
        return descriptions

    def getAbilityName(self, soupResults):
        names = []
        ability = soupResults.find_all("div", class_ = "ability-header")
        for i in range(len(ability)):
            if (i != len(ability)-1) and (ability[i+1].get_text().strip() != ability[i].get_text().strip()):
                names.append(ability[i].get_text().strip())
            elif i == len(ability)-1:
                names.append(ability[i].get_text().strip())
        return names