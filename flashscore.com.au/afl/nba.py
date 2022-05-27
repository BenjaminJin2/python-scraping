from selenium import webdriver
import pandas as pd
import time
import os
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

if os.path.exists("stats.csv"):
    os.remove("stats.csv")
columns = ['Player', 'Team', 'PTS', 'REB', 'AST', 'MIN', 'FGM', 'FGA', '2PM', '2PA', '3PM', '3PA', 'FTM', 'FTA', '+/-']
df = pd.DataFrame(columns = columns)
df.to_csv('stats.csv', mode = 'a', header = True, index = False, encoding = 'utf-8-sig')

driver = webdriver.Chrome('chromedriver.exe')
url = 'https://www.flashscore.com.au/basketball/usa/nba/results/'
driver.get(url)
time.sleep(15)

res = BeautifulSoup(driver.page_source, 'html.parser')

while (res.find('a', {'class':'event__more event__more--static'})):
    try:
        # link = driver.find_element_by_class_name("event__more")
        link = driver.find_element(By.CLASS_NAME, "event__more")
        link.click()
        time.sleep(15)
    except:
        break

res = BeautifulSoup(driver.page_source, 'html.parser')
urls = res.find_all('div', {'class':'event__match event__match--static event__match--twoLine'})

for url in urls:
    suburl = url.attrs['id'][4:]
    suburl = "https://www.flashscore.com.au/match/" + suburl + "/#/match-summary/match-summary"

    # print(suburl)
    driver.get(suburl)
    time.sleep(3)

    res = BeautifulSoup(driver.page_source, 'html.parser')

    # date = res.find('div', {'class':'duelParticipant__startTime'}).text
    # teams = res.find_all('a', {'class':'participant__participantName participant__overflow'})
    # homeTeam = teams[0].text
    # awayTeam = teams[1].text
    # homeawayScore = res.find('div', {'class':'detailScore__wrapper'}).text
    # print(date, homeTeam, awayTeam, homeawayScore)

    tabGroups = res.find_all('div', {'class':'tabs__group'})

    if (tabGroups[1].text.find("Player Statistics") != -1):
        # href = driver.find_element_by_xpath('//a[text()="Player Statistics"]')
        href = driver.find_element(By.XPATH, '//a[text()="Player Statistics"]')
        href.click()
        time.sleep(2)
        res = BeautifulSoup(driver.page_source, 'html.parser')

        players = res.find_all('div', {'class':'ui-table__row playerStatsTable__row'})

        for player in players:
            name = player.find('a', {'class':'playerStatsTable__cell playerStatsTable__participantCell playerStatsTable__cell--clickable playerStatsTable__cell--shadow'}).text
            team = player.find('div', {'class':'playerStatsTable__cell playerStatsTable__teamCell'}).text
            pts = player.find('div', {'class':'playerStatsTable__cell playerStatsTable__cell--sortingColumn'}).text
            info = player.find_all('div', {'class':'playerStatsTable__cell'})

            c = {'Player':[name], 'Team':[team], 'PTS':[pts], 'REB':[info[2].text], 'AST':[info[3].text], 'MIN':[info[4].text], 'FGM':[info[5].text], 'FGA':[info[6].text], '2PM':[info[7].text], '2PA':[info[8].text], '3PM':[info[9].text], '3PA':[info[10].text], 'FTM':[info[11].text], 'FTA':[info[12].text], '+/-':[info[13].text]}
            df = pd.DataFrame(c, columns = columns)
            df.to_csv('stats.csv', mode = 'a', header = False, index = False, encoding = 'utf-8-sig')
    #         break
    # break
driver.quit()