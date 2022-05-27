from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.common.keys import Keys 
import os
from datetime import datetime
import openpyxl
import shutil
#link to web driver
driver = webdriver.Chrome('chromedriver.exe')
url = 'https://www.tradingview.com/'
driver.get(url)
driver.maximize_window()
time.sleep(3)
#click the profile icon
driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[2]/div[3]/button[1]').click()
time.sleep(3)
#click sign in                  icon-2IihgTnv
driver.find_element_by_class_name('icon-2IihgTnv').click()
time.sleep(3)
#click email
try:
    driver.find_element_by_xpath('/html/body/div[6]/div/div[2]/div/div/div/div/div/div/div[1]/div[4]/div').click()
except:
    driver.find_element_by_xpath('/html/body/div[7]/div/div[2]/div/div/div/div/div/div/div[1]/div[4]/div').click()
time.sleep(3)
#login with username and password
username = driver.find_element_by_name('username')
password = driver.find_element_by_name('password')

#enter the credentials here
username.send_keys('ddctv')
password.send_keys('5vN$2a*8o5')
time.sleep(2)
username.send_keys(Keys.RETURN)
#get charts
time.sleep(2)
driver.get('https://www.tradingview.com/chart/')
time.sleep(2)
##read the csv into pandas dataframe
df=pd.read_csv('C:/Users/Administrator/Desktop/TVTradesGrabber/example-watchlist.csv')
data=df[5:]
list_of_symbols=data[data.columns[4]].to_list()
auto=pd.DataFrame()
# run all:
# for i in list_of_symbols:
# run some (for testing):
for i in list_of_symbols:    
# for i in list_of_symbols:
    #driver.switch_to.window(driver.window_handles[0])
    driver.get(i)
    
    #checks if the strategy is opened //*[@id="footer-chart-panel"]/div[1]/div[1]/div[4]
    time.sleep(2)
    try:
        time.sleep(3)
        ht=driver.find_element_by_xpath('//*[@id="footer-chart-panel"]/div[1]/div[1]/div[4]').get_attribute('innerHTML')
        if ht[65:65+5]=='false':
            driver.find_element_by_xpath('/html/body/div[2]/div[6]/div[1]/div/div[1]/div[1]/div[4]/div').click()
            print('strategy tester is opened')
        else:
            print('strategy tester is already opened')
    except:
        time.sleep(3)
        ht=driver.find_element_by_xpath('//*[@id="footer-chart-panel"]/div[1]/div[1]/div[1]').get_attribute('innerHTML')
        if ht[65:65+5]=='false':
            driver.find_element_by_xpath('/html/body/div[2]/div[6]/div[1]/div/div[1]/div[1]/div[1]/div').click()
            print('strategy tester is opened')
        else:
            print('strategy tester is already opened')
    time.sleep(2)
    #clicks the list of trades which should copy to clip board //*[@id="bottom-area"]/div[4]/div[1]/div[6]/ul/li[3]
    try:
        driver.find_element_by_xpath('//*[@id="bottom-area"]/div[4]/div[1]/div[6]/ul/li[3]').click()
    except:
        driver.find_element_by_xpath('//*[@id="bottom-area"]/div[5]/div[1]/div[6]/ul/li[3]').click()
    time.sleep(3)
    #clicks the download icon 
    try:
        click_on_download=driver.find_element_by_xpath('/html/body/div[2]/div[6]/div[2]/div[4]/div[1]/div[5]/div').click()
    except:
        click_on_download=driver.find_element_by_xpath('/html/body/div[2]/div[6]/div[2]/div[5]/div[1]/div[5]/div').click()
    time.sleep(1)
    os.chdir('C:\\Users\\Administrator\\Downloads')
    Flag=True
    for k in os.listdir():
        if k.startswith('RSI_X-Stream_SE') and Flag==True:
            df=pd.read_csv(k)
            symbol_name=driver.find_element_by_xpath('//*[@id="header-toolbar-symbol-search"]').text
            df['Symbol']=[symbol_name for j in range(df.shape[0])]
            print(df.head())
            Flag=False
            time.sleep(2)
            # os.remove(k)
            original = "C:\\Users\\Administrator\\Downloads\\"+k
            target = "C:\\Users\\Administrator\\Desktop\\TVTradesGrabber\\"+k
            shutil.move(original,target)
    auto=auto.append(df,ignore_index=True)
#saves the appended data content in the TVTradesGrabber folder. Also, if you need to remove the option to save the data as csv, just comment out the next three (3) lines.
os.chdir('C:\\Users\\Administrator\\Desktop\\TVTradesGrabber')
now_ = datetime.now().strftime('%b_%d_%y_%H_%M_%S')
auto.to_csv('Combined_-_RSI_X-Stream_SE_1.0_' + now_ + '.csv', index=False)