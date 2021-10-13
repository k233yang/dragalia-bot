from bs4 import BeautifulSoup


class Abilities:
    def __init__(self, soupResults, isChar):
        self.abilityDescription = self.getAbilityDescription(soupResults, isChar)
        self.abilityName = self.getAbilityName(soupResults)

    def getAbilityDescription(self, soupResults, isChar):
        descriptions = []
        ability = soupResults.find_all("div", class_ = "ability-table")
        for k in range(len(ability)):
            firstAbility = ability[k].get_text().strip()
            AbilityParts = []
            track = 0
            j = 0
            #Adding every line separated by a newline to a list
            for i in range(len(firstAbility)):
                if firstAbility[i] == '\n':
                    AbilityParts.append(firstAbility[track:i])
                    track += j
                    j = 0
                elif i == len(firstAbility) -1:
                    AbilityParts.append(firstAbility[track:i+1])
                j+=1
            
            #Checking list for ability descriptions and hardcoding indexes
            for i in range(len(AbilityParts)):
                #print("Index "+ str(i) + " " + AbilityParts[i])
                #For some reason the chain coabs has different indexing than the other abilities/coabs
                if k == 1 and (i+4)%7 == 0 and i >= 10 :
                    #print("Index "+ str(i) + " " + AbilityParts[i])
                    #print(AbilityParts[0].lstrip()+" Lv"+str((i+4)/7 -1)[0])
                    #print(AbilityParts[i][1:])
                    descriptions.append(AbilityParts[i][1:])
                #Every 6th, 13th, 20th, etc index will have the Ability description
                elif k!=1 and (i+1)%7 == 0:
                    #print("Index "+ str(i) + " " + AbilityParts[i])
                    #print(AbilityParts[2].lstrip()+" Lv"+str((i+1)/7)[0])
                    #print(AbilityParts[i][1:])
                    descriptions.append(AbilityParts[i][1:])
                elif (i+1)%7 == 0 and isChar == False:
                    #print("Index "+ str(i) + " " + AbilityParts[i])
                    descriptions.append(AbilityParts[i][1:])

        for i in range(len(descriptions)):
            descriptions[i] = descriptions[i].replace(".If", ".\n\nIf")
            descriptions[i] = descriptions[i].replace(". If", ".\n\nIf")
            descriptions[i] = descriptions[i].replace(".  If", ".\n\nIf")

            descriptions[i] = descriptions[i].replace(". This", ".\n\nThis")
            descriptions[i] = descriptions[i].replace(".This", ".\n\nThis")

            descriptions[i] = descriptions[i].replace(".When", ".\n\nWhen")
            descriptions[i] = descriptions[i].replace(". When", ".\n\nWhen")

            descriptions[i] = descriptions[i].replace(". Also", ".\n\nAlso")
            descriptions[i] = descriptions[i].replace(".Also", ".\n\nAlso")

            descriptions[i] = descriptions[i].replace("・", "\n\n・")
            descriptions[i] = descriptions[i].replace(":・", "\n\n・")
                                
            descriptions[i] = descriptions[i].replace(".Lv", ".\n\nLv")
            descriptions[i] = descriptions[i].replace(".In", ".\n\nIn")
                                
            descriptions[i] = descriptions[i].replace("%The", "%\n\nThe")
            descriptions[i] = descriptions[i].replace(". The", ".\n\nThe")

            descriptions[i] = descriptions[i].replace(".Phase", ".\n\nPhase")
            descriptions[i] = descriptions[i].replace(". Phase", ".\n\nPhase")
            
            descriptions[i] = descriptions[i].replace(".-", ".\n\n-")
            descriptions[i] = descriptions[i].replace(". -", ".\n\n-")

            descriptions[i] = descriptions[i].replace(".)", ".)\n\n")
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