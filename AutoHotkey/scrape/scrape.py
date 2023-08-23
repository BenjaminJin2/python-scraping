from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
import pyperclip

# Get the URL from the clipboard
url = pyperclip.paste()

# Display the URL
print("The URL of the active tab is:", url)

# Send a GET request to the website you want to scrape
# url = "https://www.fakexy.com/"  # Replace with the actual URL
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Extract the required data from the HTML

columns = []
values = []
data = {}
td_tags = soup.find_all('td')

for i in range(0, len(td_tags), 2):
    key = td_tags[i].text.strip()
    value = td_tags[i + 1].text.strip()
    columns.append(key)
    values.append(value)
    data[key] = value

# print(columns)
# print(values)


# You need to disable these codes below when you star first.

#
if os.path.exists("out.csv"):
    os.remove("out.csv")
df = pd.DataFrame(columns = columns)
df.to_csv('out.csv', mode = 'a', header = True, index = False, encoding = 'utf-8-sig')
#

df = pd.DataFrame([data], columns = columns)
df.to_csv('out.csv', mode = 'a', header = False, index = False, encoding = 'utf-8-sig')