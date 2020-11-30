# Selenium Scrapper
import re
from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd


PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

symbols = []
pricesClose = []
pricesOpen = []
pricesHigh =[]
pricesLow =[]
driver.get("https://www.bankier.pl/gielda/notowania/akcje")

content = driver.page_source
soup = BeautifulSoup(content)

tr = soup.findAll('tr')
closeCourse = re.compile('.*colKurs change.*')

for row in tr:
    a = row.find('a', title=True)
    close = row.find('td', class_=closeCourse)
    open = row.find('td', attrs='colOtwarcie')
    high = row.find('td', attrs='calMaxi')
    low = row.find('td', attrs='calMini')
    if a != None:
       symbols.append(a.text)
    if close != None:
        pricesClose.append(close.text)
    if open != None:
        pricesOpen.append((open.text))
    if high != None:
        pricesHigh.append((high.text))
    if low != None:
        pricesLow.append((low.text))


df = pd.DataFrame({'Symbol spółki':symbols,'Cena zamknięcia':pricesClose, 'Cena otwarcia':pricesOpen, 'Cena najwyższa':pricesHigh, 'Cena najniższa':pricesLow})
todayDate = datetime.now().date()
todayTime = datetime.now().time()
endSessionTime = todayTime.replace(hour=17, minute=0, second=0, microsecond=0)
if todayTime > endSessionTime:
    df.to_csv('stockPrices_' + todayDate.strftime("%Y%m%d") + '.csv', index=False, encoding='utf-8')
