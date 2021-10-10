from bs4 import BeautifulSoup

class Stats:
    iconURL = ""
    altURL = ""
    title = ""
    def __init__(self, soupResults, soupResults2, links, soup):
        self.hp = self.getHp(soupResults)
        self.str = self.getStr(soupResults)
        self.element = self.getElement(soupResults2)
        self.weapon = self.getWeapon(soupResults2)
        self.getIcons(links, soup)

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

    # SCRAPING ICON
    def getIcons(self, links, soup):
        for a in links:
            # ADVENTURER ID
            if('r05' in a['href'] or 'r04'in a['href'] or 'r03' in a['href']):
                #print("Found the URL:", a['href'])
                self.title = soup.find('title').get_text().replace("- Adventurer", '')
                charID = a['href'].replace("/w", '')[:-17]
                charID = charID[6:]
                #print("CharID: " + charID)
                self.iconURL = "https://yvsdrop.github.io/dl-assets/storysprites/"+charID+"/"+charID+".png"
                break
            #DRAGON ID
            elif('_01' in a['href']):
                #print("Found the URL:", a['href'])
                self.title = soup.find('title').get_text().replace("- Dragon", '')
                charID = a['href'].replace("/w", '')[:-13]
                charID = charID[6:]
                #print("CharID: " + charID)
                self.iconURL = "https://yvsdrop.github.io/dl-assets/storysprites/"+charID+"/"+charID+".png"
                # Sometimes URL above breaks, for contingency
                self.altURL = "https://yvsdrop.github.io/dl-assets/storysprites/"+charID+"/"+charID+"_parts_c000.png"
                break
