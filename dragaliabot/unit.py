from bs4 import BeautifulSoup
import stats

class Unit:
    def __init__(self, soupResults, soupResults2):
        self.charStats = stats.Stats(soupResults, soupResults2)
