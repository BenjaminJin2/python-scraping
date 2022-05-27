from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

if os.path.exists("out.csv"):
    os.remove("out.csv")
columns = ['Date', 'HomeTeam', 'AwayTeam', 'MatchInfo', 'TotalScore', 'Over 1', 'Over 2', 'Over 3', 'Over 4', 'Over 5', 'Over 6', 'Over 7', 'Over 8', 'Over 9', 'Over 10', 'Over 11', 'Over 12', 'Over 13', 'Over 14', 'Over 15', 'Over 16', 'Over 17', 'Over 18', 'Over 19', 'Over 20']
df = pd.DataFrame(columns = columns)
df.to_csv('out.csv', mode = 'a', header = True, index = False, encoding = 'utf-8-sig')

driver = webdriver.Chrome('chromedriver.exe')
suburl = "https://www.flashscore.com.au/match/p4QGBgF4/#match-summary/match-summary"
driver.get(suburl)
time.sleep(2)

res = BeautifulSoup(driver.page_source, 'html.parser')

date = res.find('div', {'class':'duelParticipant__startTime'}).text

teams = res.find_all('a', {'class':'participant__participantName participant__overflow'})
homeTeam = teams[0].text
awayTeam = teams[1].text

matchInfo = ""
if (res.find('div', {'class':'mi__data'})):
    matchInfo = res.find('div', {'class':'mi__data'}).text

homeScore = res.find('div', {'class':'smh__part smh__home smh__score smh__score--left'}).text
awayScore = res.find('div', {'class':'smh__part smh__away smh__score smh__score--left'}).text
homes = homeScore.split("/")
aways = awayScore.split("/")

tabGroups = res.find_all('div', {'class':'tabs__group'})
    if (tabGroups[1].text.find("Ball by Ball") != -1):
        href = driver.find_element_by_xpath('//a[text()="Ball by Ball"]')
        href.click()
        time.sleep(1)

        res = BeautifulSoup(driver.page_source, 'html.parser')
        overs1 = res.find_all('div', {'class':'bbb__overs'})
        runs1 = res.find_all('div', {'class':'bbb__runs'})

        Innings = res.find_all('a', {'class':'subTabs__tab'})
        if (len(Innings) != 1):
            elements = driver.find_elements_by_class_name("subTabs__tab")
            elements[0].click()
            time.sleep(1)
            
            res = BeautifulSoup(driver.page_source, 'html.parser')
            overs0 = res.find_all('div', {'class':'bbb__overs'})
            runs0 = res.find_all('div', {'class':'bbb__runs'})
        else:
            overs0 = []
            runs0 =[]

    if (homes[0]):
        home = int(homes[0])
    else:
        home = 0
    if (aways[0]):
        away = int(aways[0])
    else:
        away = 0

    if (home < away):
        runsTemp = runs0
        runs0 = runs1
        runs1 = runsTemp
        oversTemp = overs0
        overs0 = overs1
        overs1 = oversTemp

c = {'Date':[date], 'HomeTeam':[homeTeam], 'AwayTeam':[awayTeam], 'MatchInfo':[matchInfo], 'TotalScore':[homeScore]}
i = 0
for run in runs1:
    c[overs1[i].text] = [run.text]
    i = i + 1
df = pd.DataFrame(c, columns = columns)
df.to_csv('out.csv', mode = 'a', header = False, index = False, encoding = 'utf-8-sig')

c = {'Date':[date], 'HomeTeam':[homeTeam], 'AwayTeam':[awayTeam], 'MatchInfo':[matchInfo], 'TotalScore':[awayScore]}
i = 0
for run in runs0:
    c[overs0[i].text] = [run.text]
    i = i + 1
df = pd.DataFrame(c, columns = columns)
df.to_csv('out.csv', mode = 'a', header = False, index = False, encoding = 'utf-8-sig')

driver.quit()