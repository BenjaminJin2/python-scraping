from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

url = "https://www.fakexy.com/"

time.sleep(20)

driver.get(url)

element = driver.find_element(By.ID, "in-page-channel-node-id")

print(element.text)

driver.puit()