import requests
from bs4 import BeautifulSoup
import pandas as pd

RANKINGS_URL = "https://www.transfermarkt.co.uk/statistik/weltrangliste"

BASE_URL_PART_I = "https://www.transfermarkt.co.uk/statistik/weltrangliste/statistik/stat/ajax/yw1/datum/"
BASE_URL_PART_II = "/plus/0/page/"

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

page = RANKINGS_URL
tree = requests.get(page, headers=headers)
soup = BeautifulSoup(tree.content, 'html.parser')

dropdown = soup.find("select",{"name":"datum"})
dates = dropdown.find_all("option")

dateList = []

for i in range(0, len(dates)):
    dateList.append(dates[i].get("value"))

count = 0

for date in dateList:
    print(date)
    # Initialise lists
    RankList = []
    TeamList = []
    PointsList = []

    for i in range(1,10):
        #Take site and structure html
        #page = playerLinks[i]
        page = BASE_URL_PART_I + date + BASE_URL_PART_II + str(i)
        tree = requests.get(page, headers=headers)
        soup = BeautifulSoup(tree.content, 'html.parser')
        
        #Let's look at the first name in the Players list.
        Rank = soup.find_all("td", {"class": "zentriert cp"})
        Team = soup.find_all("td", {"class": "hauptlink"})
        Points = soup.find_all("td", {"class": "zentriert hauptlink"})
        
        for i in range(0,len(Rank)):
            RankList.append(Rank[i].text)
            TeamList.append(Team[i*2].text)
            PointsList.append(Points[i].text)
          
    df = pd.DataFrame({"Rank":RankList,"Points":PointsList,"Team":TeamList})
    
    if df.shape[0] > 0:
        df.loc[:, 'Date'] = date
        df = df[['Date', 'Rank', 'Team', 'Points']]
    
        if count == 0:
            df_all = df
            count = 1
        else:
            df_all = df_all.append(df)
        
df_all.to_excel('world_rankings.xlsx', encoding='utf8')