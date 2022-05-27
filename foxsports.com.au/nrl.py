from selenium import webdriver
import pandas as pd
import time
import os
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

if os.path.exists("stats.csv"):
    os.remove("stats.csv")
columns = ['Date', 'Team', 'Name', 'T', 'G', 'RM', 'PTS', 'TCK', 'R', 'PCM', 'LB', 'LBA', 'TA', 'KM', 'FD', 'SC']
df = pd.DataFrame(columns = columns)
df.to_csv('stats.csv', mode = 'a', header = True, index = False, encoding = 'utf-8-sig')

driver = webdriver.Chrome('chromedriver.exe')
# url = 'https://www.foxsports.com.au/score-centre/nrl/'
# driver.get(url)
# time.sleep(15)

# res = BeautifulSoup(driver.page_source, 'html.parser')


suburl = "https://www.foxsports.com.au/nrl/nrl-premiership/match-centre/NRL20220502/playerstats"
driver.get(suburl)
time.sleep(5)

res = BeautifulSoup(driver.page_source, 'html.parser')

trs = res.find_all('tr')

for tr in trs:
    info = tr.find_all('td')
    if info.len != 0:
        date = "date"
        team = "team"
        print(info)
    # c = {'Date':[date], 'Team':[team], 'Name':[info[1].text], 'T':[info[2].text], 'G':[info[3].text], 'RM':[info[4].text], 'PTS':[info[5].text], 'TCK':[info[6].text], 'R':[info[7].text], 'PCM':[info[8].text], 'LB':[info[9].text], 'LBA':[info[10].text], 'TA':[info[11].text], 'KM':[info[12].text], 'FD':[info[13].text], 'SC':[info[14].text]}
    # c = {'Date':[date], 'Team':[team], 'Name':[info[1].text], 'T':[info[2].text], 'G':[info[3].text], 'RM':[info[4].text], 'PTS':[info[5].text], 'TCK':[info[6].text], 'R':[info[7].text], 'PCM':[info[8].text], 'LB':[info[9].text], 'LBA':[info[10].text], 'TA':[info[11].text], 'KM':[info[12].text], 'FD':[info[13].text], 'SC':[info[0].text]}
    # c = {'Date':[date], 'Team':[team], 'Name':'saa', 'T':'saa', 'G':'saa', 'RM':'saa', 'PTS':'saa', 'TCK':'saa', 'R':'saa', 'PCM':'saa', 'LB':'saa', 'LBA':'saa', 'TA':'saa', 'KM':'saa', 'FD':'saa', 'SC':'saa'}
    # df = pd.DataFrame(c, columns = columns)
    # df.to_csv('stats.csv', mode = 'a', header = False, index = False, encoding = 'utf-8-sig')
