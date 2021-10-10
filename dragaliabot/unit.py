from bs4 import BeautifulSoup
import stats
import skills

class Unit:
    def __init__(self, soupResults, soupResults2, links, soup):
        self.charStats = stats.Stats(soupResults, soupResults2, links, soup)
        self.charSkills = skills.Skills(soupResults)
