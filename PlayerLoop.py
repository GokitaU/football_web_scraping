import requests
from bs4 import BeautifulSoup
from os.path  import basename
import pandas as pd
from datetime import datetime

BASE_URL = "https://www.transfermarkt.co.uk"

def convert_to_datetime(text):
    date = datetime.strptime(text, '%b %d, %Y')
    return date

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

#Process League Table
page = 'https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1'
tree = requests.get(page, headers = headers)
soup = BeautifulSoup(tree.content, 'html.parser')

#Create an empty list to assign these values to
teamLinks = []

#Extract all links with the correct CSS selector
links = soup.select("a.vereinprofil_tooltip")

#We need the location that the link is pointing to, so for each link, take the link location. 
#Additionally, we only need the links in locations 1,3,5,etc. of our list, so loop through those only
for i in range(len(links)):
    teamLinks.append(links[i].get("href"))

teamLinks = list(set(teamLinks))

#For each location that we have taken, add the website before it - this allows us to call it later
for i in range(len(teamLinks)):
    teamLinks[i] = BASE_URL + teamLinks[i]

teamLinks = list(set(teamLinks))

print('Team List found')

#Create an empty list for our player links to go into
playerLinks = []

#Run the scraper through each of our 20 team links
for i in range(len(teamLinks)):

    #Download and process the team page
    page = teamLinks[i]
    tree = requests.get(page, headers = headers)
    soup = BeautifulSoup(tree.content, 'html.parser')

    #Extract all links
    links = soup.select("a.spielprofil_tooltip")   
    
    #For each link, extract the location that it is pointing to
    for j in range(len(links)):
        playerLinks.append(links[j].get("href"))
        
    #The page list the players more than once - let's use list(set(XXX)) to remove the duplicates
    playerLinks = list(set(playerLinks))

print('Player List found')
    
count = 0

for i in range(len(playerLinks)):
    #Take site and structure html
    #page = playerLinks[i]
    page = BASE_URL + playerLinks[i]
    tree = requests.get(page, headers=headers)
    soup = BeautifulSoup(tree.content, 'html.parser')
    
    name = soup.find_all("h1", {"itemprop": "name"})
    if count % 25 == 0:
        print(name[0].text)
    
    #Let's look at the first name in the Players list.
    TransferDate = soup.find_all("td", {"class": "zentriert hide-for-small"})
    Fee = soup.find_all("td", {"class": "zelle-abloese"})
    Clubs = soup.find_all("td", {"class": "hauptlink no-border-links hide-for-small vereinsname"})

    # Initialise lists
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
    
    if df.shape[0] > 0:
        df.loc[:, 'PlayerName'] = name[0].text
        df = df[['PlayerName', 'TransferDate', 'Fees', 'Left', 'Joined']]
    
        if count == 0:
            df_all = df
        else:
            df_all = df_all.append(df)
        
        count += 1

df_all['TransferDate'] = df_all['TransferDate'].apply(convert_to_datetime)

def convert_if_string(value):
    if isinstance(value, str):
        value = value.strip()
    return value

for col in df_all:
    df_all[col] = df_all[col].apply(convert_if_string)
    
df_all.to_excel('test.xlsx', encoding='utf8')
