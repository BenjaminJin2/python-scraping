from selenium import webdriver
import pandas as pd
import time
import os
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta

if os.path.exists("out.csv"):
    os.remove("out.csv")
columns = ['Date', 'HomeTeam', 'AwayTeam', 'Q1HomeScore', 'Q2HomeScore', 'Q3HomeScore', 'Q4HomeScore', 'Q5HomeScore', 'Q1AwayScore', 'Q2AwayScore', 'Q3AwayScore', 'Q4AwayScore', 'Q5AwayScore']
df = pd.DataFrame(columns = columns)
df.to_csv('out.csv', mode = 'a', header = True, index = False, encoding = 'utf-8-sig')

# url = 'https://www.flashscore.com.au/afl/australia/afl-women/results/'
# url = 'https://www.flashscore.com.au/basketball/usa/nba/results/'
# url = 'https://www.flashscore.com.au/afl/australia/afl-2021/results/'
# url = 'https://www.flashscore.com.au/rugby/england/premiership-rugby/results/'
# 

url = input("Enter URL:")

driver = webdriver.Chrome('chromedriver.exe')
time.sleep(1)

driver.get(url)
time.sleep(15)

res = BeautifulSoup(driver.page_source, 'html.parser')
while (res.find('a', {'class':'event__more event__more--static'})):
    try:
        link = driver.find_element(By.CLASS_NAME, "event__more")
        link.click()
        time.sleep(15)
    except:
        break

res = BeautifulSoup(driver.page_source, 'html.parser')

header_block = driver.find_element(By.ID, "hamburger-menu")
header_block.click()
time.sleep(1)

menu_settings = driver.find_element(By.ID, "hamburger-menu-settings")
menu_settings.click()
time.sleep(1)

res = BeautifulSoup(driver.page_source, 'html.parser')
tzActual = res.find("div", {"id": "tzActual"})

timezone = tzActual.text
gmt = timezone.find("GMT")
subT = float(timezone[gmt+4:])

close_set = driver.find_element(By.ID, "lsid-window-close")
close_set.click()
time.sleep(1)

res = BeautifulSoup(driver.page_source, 'html.parser')
urls = res.find_all('div', {'class':'event__match--twoLine'})

for url in urls:
    time_text = url.find('div', {'class':'event__time'}).text
    time_str = time_text[:12]
    date_format_str = '%d.%m. %H:%M'
    given_time = datetime.strptime(time_str, date_format_str)
    final_time = given_time - timedelta(hours=subT)
    date = final_time.strftime('%d.%m. %H:%M')

    homeTeam = url.find('div', {'class':'event__participant--home'}).text
    awayTeam = url.find('div', {'class':'event__participant--away'}).text
    
    q1homeScore = ""
    q1awayScore = ""
    q1 = url.find('div', {'class':'event__part event__part--home event__part--1'})
    if q1:
        q1homeScore = url.find('div', {'class':'event__part event__part--home event__part--1'}).text
        q1awayScore = url.find('div', {'class':'event__part event__part--away event__part--1'}).text
    
    q2homeScore = ""
    q2awayScore = ""
    q2 = url.find('div', {'class':'event__part event__part--home event__part--1'})
    if q2:
        q2homeScore = url.find('div', {'class':'event__part event__part--home event__part--2'}).text
        q2awayScore = url.find('div', {'class':'event__part event__part--away event__part--2'}).text
    
    q3homeScore = ""
    q3awayScore = ""
    q3 = url.find('div', {'class':'event__part event__part--home event__part--3'})
    if q3:
        q3homeScore = url.find('div', {'class':'event__part event__part--home event__part--3'}).text
        q3awayScore = url.find('div', {'class':'event__part event__part--away event__part--3'}).text
    
    q4homeScore = ""
    q4awayScore = ""
    q4 = url.find('div', {'class':'event__part event__part--home event__part--4'})
    if q4:
        q4homeScore = url.find('div', {'class':'event__part event__part--home event__part--4'}).text
        q4awayScore = url.find('div', {'class':'event__part event__part--away event__part--4'}).text

    q5homeScore = ""
    q5awayScore = ""
    q5 = url.find('div', {'class':'event__part event__part--home event__part--5'})
    if q5:
        q5homeScore = url.find('div', {'class':'event__part event__part--home event__part--5'}).text
        q5awayScore = url.find('div', {'class':'event__part event__part--away event__part--5'}).text
    # print(date, homeTeam, awayTeam, q1homeScore, q2homeScore, q3homeScore, q4homeScore, q5homeScore, q1awayScore, q2awayScore, q3awayScore, q4awayScore, q5awayScore)

    c = {'Date':[date], 'HomeTeam':[homeTeam], 'AwayTeam':[awayTeam], 'Q1HomeScore':[q1homeScore], 'Q2HomeScore':[q2homeScore], 'Q3HomeScore':[q3homeScore], 'Q4HomeScore':[q4homeScore], 'Q5HomeScore':[q5homeScore], 'Q1AwayScore':[q1awayScore], 'Q2AwayScore':[q2awayScore], 'Q3AwayScore':[q3awayScore], 'Q4AwayScore':[q4awayScore], 'Q5AwayScore':[q5awayScore]}
    df = pd.DataFrame(c, columns = columns)
    df.to_csv('out.csv', mode = 'a', header = False, index = False, encoding = 'utf-8-sig')

driver.quit()