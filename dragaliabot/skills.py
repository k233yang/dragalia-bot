from bs4 import BeautifulSoup

class Skills:
    def __init__(self, soupResults):
        self.skillDescription = self.getSkillDesc(soupResults)
        self.skillDet = self.getSkillDetails(soupResults)

    def getSkillDesc(self, results):
        #To Parse
        skillTable = []
        #Contains Skill Description
        skillDesc = []
        temp = []
        test = results.find_all("div", class_="skill-table")
        for res in test:
            skillTable.append(res.text.split('\n\n'))

        #Skill Desciption & Details
        for i in range(len(skillTable)):
            temp.append(skillTable[i][-4])

            #Removes preceding skill details
            desc = skillTable[i][-3].split('\n')
            skillDesc.append(desc[-1])
                        
        #Formatting Skill Desc
        for i in range(len(skillDesc)):
            skillDesc[i] = skillDesc[i].replace(".If", ".\n\nIf")
            skillDesc[i] = skillDesc[i].replace(". If", ".\n\nIf")
            skillDesc[i] = skillDesc[i].replace(".  If", ".\n\nIf")

            skillDesc[i] = skillDesc[i].replace(". This", ".\n\nThis")
            skillDesc[i] = skillDesc[i].replace(".This", ".\n\nThis")

            skillDesc[i] = skillDesc[i].replace(".When", ".\n\nWhen")
            skillDesc[i] = skillDesc[i].replace(". When", ".\n\nWhen")

            skillDesc[i] = skillDesc[i].replace(". Also", ".\n\nAlso")
            skillDesc[i] = skillDesc[i].replace(".Also", ".\n\nAlso")

            skillDesc[i] = skillDesc[i].replace("・", "\n\n・")
            skillDesc[i] = skillDesc[i].replace(":・", "\n\n・")
                                
            skillDesc[i] = skillDesc[i].replace(".Lv", ".\n\nLv")
            skillDesc[i] = skillDesc[i].replace(".In", ".\n\nIn")
                                
            skillDesc[i] = skillDesc[i].replace("%The", "%\n\nThe")
            skillDesc[i] = skillDesc[i].replace(". The", ".\n\nThe")

            skillDesc[i] = skillDesc[i].replace(".Phase", ".\n\nPhase")
            skillDesc[i] = skillDesc[i].replace(". Phase", ".\n\nPhase")

        return skillDesc

    def getSkillDetails(self, results):
        #To Parse
        skillTable = []

        #Contains Skill SP Cost
        skillDetails = []
        temp = []

        test = results.find_all("div", class_="skill-table")
        for res in test:
            skillTable.append(res.text.split('\n\n'))

        for i in range(len(skillTable)):
            temp.append(skillTable[i][-4])

        test = results.find_all("div", class_="skill-table")
        for res in test:
            skillTable.append(res.text.split('\n\n'))

        #Cleaning
        for i in temp:
            skillDetails.append(i.split('\n'))

        return skillDetails