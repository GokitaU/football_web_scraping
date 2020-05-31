import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

page = "https://www.transfermarkt.co.uk/a/transfers/spieler/7767"

pageTree = requests.get(page, headers=headers)
pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

Players = pageSoup.find_all("h1", {"itemprop": "name"})

print(Players[0].text)

#Let's look at the first name in the Players list.
TransferDate = pageSoup.find_all("td", {"class": "zentriert hide-for-small"})

Fee = pageSoup.find_all("td", {"class": "zelle-abloese"})

Clubs = pageSoup.find_all("td", {"class": "hauptlink no-border-links hide-for-small vereinsname"})


TransferDateList = []
FeeList = []
LeftList = []
JoinedList = []

for i in range(0,len(Fee)):
    TransferDateList.append(TransferDate[(i*3)+1].text)
    FeeList.append(Fee[i].text)
    LeftList.append(Clubs[i*2].text)
    JoinedList.append(Clubs[(i*2)+1].text)
    
df = pd.DataFrame({"TransferDate":TransferDateList,"Fees":FeeList,"Left":LeftList,"Joined":JoinedList})
df.loc[:, 'PlayerName'] = Players[0].text
df = df[['PlayerName', 'TransferDate', 'Fees', 'Left', 'Joined']]


