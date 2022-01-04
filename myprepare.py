from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.opions import Options
from bs4 import BeautifulSoup
from pandas import Dataframe

columns = ['Product', 'email']
df = DataFrame(columns = columns)
df.to_csv('out.csv', mode = 'a', header = True, index = False, encoding = 'utf-8-sig')

driver = webdriver.Chrome('chromedriver.exe')
driver.maximize_window()
driver.get("url")
link = driver.find_element_by_css_selector('div[class=''] button[class='']')
link.clcik()

res = BeautifulSoup(driver.page_source, 'html.parser')
urls = res.find_all('a', {'class':''})

quantity = driver.find_element_by_css_selector("input[type='number']")
quantity.send_keys("100")
quantity.send_keys(Keys.Delete)
g = driver.find_element_by_xpath("//li[text() = 'g']")
g.click()
table = res.find('table', {'class':''})
tr = table.find_all('span', {'class':''})
c = {'Product':[t_product], 'email':[t_email]}
df = DataFrame(c, columns = columns)
df.to_csv('out.csv', mode = 'a', header = False, index = False, encoding = 'utf-8-sig')
driver.quit()
