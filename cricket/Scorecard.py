from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

if os.path.exists("scores.csv"):
    os.remove("scores.csv")
columns = ['Date', 'HomeTeam', 'AwayTeam', 'Team', 'Batsman', 'Status', 'R', 'B', 'Min', '4s', '6s']
df = pd.DataFrame(columns = columns)
df.to_csv('scores.csv', mode = 'a', header = True, index = False, encoding = 'utf-8-sig')

driver = webdriver.Chrome('chromedriver.exe')
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
    time.sleep(2)

    res = BeautifulSoup(driver.page_source, 'html.parser')

    date = res.find('div', {'class':'duelParticipant__startTime'}).text

    teams = res.find_all('a', {'class':'participant__participantName participant__overflow'})
    homeTeam = teams[0].text
    awayTeam = teams[1].text

    tabGroups = res.find_all('div', {'class':'tabs__group'})
    if (tabGroups[1].text.find("Scorecard") != -1):
        href = driver.find_element_by_xpath('//a[text()="Scorecard"]')
        href.click()
        time.sleep(2)

        res = BeautifulSoup(driver.page_source, 'html.parser')
        team = res.find('a', {'class':'subTabs__tab selected'}).text
        parseData = res.find('div', {'class':'ui-table playerStatsCricketTable___2rpZLKe'})
        pageData = parseData.find_all('div', {'class':'ui-table__row row___3H-IoJs'})
        for data in pageData:
            batsMan = data.find('div', {'class':'rowCellPlayer___1gWVVS4'}).text
            status = data.find('div', {'class':'rowCellStatus___3ivTMGI'}).text
            values = data.find_all('div', {'class':'rowCell___2gpHV6I'})
            r = values[0].text
            b = values[1].text
            min = values[2].text
            fours = values[3].text
            sixs = values[4].text
            # print(team, batsMan, status, r, b, min, fours, sixs)
            c = {'Date':[date], 'HomeTeam':[homeTeam], 'AwayTeam':[awayTeam], 'Team':[team], 'Batsman':[batsMan], 'Status':[status], 'R':[r], 'B':[b], 'Min':[min], '4s':[fours], '6s':[sixs]}
            df = pd.DataFrame(c, columns = columns)
            df.to_csv('scores.csv', mode = 'a', header = False, index = False, encoding = 'utf-8-sig')

        Innings = res.find_all('a', {'class':'subTabs__tab'})
        if (len(Innings) != 1):
            elements = driver.find_elements_by_class_name("subTabs__tab")
            elements[0].click()
            time.sleep(1)
            
            res = BeautifulSoup(driver.page_source, 'html.parser')
            team = res.find('a', {'class':'subTabs__tab selected'}).text
            parseData = res.find('div', {'class':'ui-table playerStatsCricketTable___2rpZLKe'})
            pageData = parseData.find_all('div', {'class':'ui-table__row row___3H-IoJs'})
            for data in pageData:
                batsMan = data.find('div', {'class':'rowCellPlayer___1gWVVS4'}).text
                status = data.find('div', {'class':'rowCellStatus___3ivTMGI'}).text
                values = data.find_all('div', {'class':'rowCell___2gpHV6I'})
                r = values[0].text
                b = values[1].text
                min = values[2].text
                fours = values[3].text
                sixs = values[4].text
                c = {'Date':[date], 'HomeTeam':[homeTeam], 'AwayTeam':[awayTeam], 'Team':[team], 'Batsman':[batsMan], 'Status':[status], 'R':[r], 'B':[b], 'Min':[min], '4s':[fours], '6s':[sixs]}
                df = pd.DataFrame(c, columns = columns)
                df.to_csv('scores.csv', mode = 'a', header = False, index = False, encoding = 'utf-8-sig')

driver.quit()