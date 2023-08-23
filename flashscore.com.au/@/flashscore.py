from selenium import webdriver
import pandas as pd
import time
import os
from bs4 import BeautifulSoup

if os.path.exists("out.csv"):
    os.remove("out.csv")
columns = ['Date', 'HomeTeam', 'AwayTeam', 'MatchInfo', 'HomeScore', 'AwayScore', 'HomeOverNumber', 'HomeOverRuns', 'AwayOverNumber', 'AwayOverRuns']
df = pd.DataFrame(columns = columns)
df.to_csv('out.csv', mode = 'a', header = True, index = False, encoding = 'utf-8-sig')

# driver = webdriver.Chrome('chromedriver.exe')
driver = webdriver.Chrome()
url = 'https://www.flashscore.com.au/cricket/world/twenty20-international/results/'
driver.get(url)
time.sleep(3)

res = BeautifulSoup(driver.page_source, 'html.parser')
urls = res.find_all('div', {'class':'event__match event__match--static event__match--twoLine'})

for url in urls:
    suburl = url.attrs['id'][5:]
    suburl = "https://www.flashscore.com.au/match/" + suburl + "/#match-summary/match-summary"
    print(suburl)

    driver.get(suburl)
    time.sleep(1)

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

    homeOverNumber = ""
    homeOverRuns = ""
    awayOverNumber = ""
    awayOverRuns = ""

    tabGroups = res.find_all('div', {'class':'tabs__group'})
    if (tabGroups[1].text.find("Ball by Ball") != -1):
        href = driver.find_element_by_xpath('//a[text()="Ball by Ball"]')
        href.click()
        time.sleep(1)
        res = BeautifulSoup(driver.page_source, 'html.parser')
        overs = res.find_all('div', {'class':'bbb__overs'})
        runs = res.find_all('div', {'class':'bbb__runs'})

        homeOverNumber = overs[0].text
        homeOverRuns = runs[0].text
        awayOverNumber = overs[0].text
        awayOverRuns = runs[0].text

    c = {'Date':[date], 'HomeTeam':[homeTeam], 'AwayTeam':[awayTeam], 'MatchInfo':[matchInfo], 'HomeScore':[homeScore], 'AwayScore':[awayScore], 'HomeOverNumber':[homeOverNumber], 'HomeOverRuns':[homeOverRuns], 'AwayOverNumber':[awayOverNumber], 'AwayOverRuns':[awayOverRuns]}
    df = pd.DataFrame(c, columns = columns)
    df.to_csv('out.csv', mode = 'a', header = False, index = False, encoding = 'utf-8-sig')

driver.quit()