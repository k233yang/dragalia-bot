from bs4 import BeautifulSoup
import stats
import skills
import abilities

class Unit:
    def __init__(self, soupResults, soupResults2, links, soup):
        self.charStats = stats.Stats(soupResults, soupResults2, links, soup)
        self.charSkills = skills.Skills(soupResults)
        self.charAbilities = abilities.Abilities(soupResults)
