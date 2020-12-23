'''
NYP Google DSC Mini Projects
Web Scraping Project of COVID-19 Data
'''

# importing modules Requests, BeautifulSoup, sqlite3


import requests 
from bs4 import BeautifulSoup
import sqlite3



conn = sqlite3.connect('data.sqlite')
cur = conn.cursor()

#Delete table to ensure data is updated each time you run this file
cur.execute('DROP TABLE IF EXISTS Data')
cur.execute('DROP TABLE IF EXISTS Date')


#Create the table 
cur.execute('''CREATE TABLE Data
    (country TEXT UNIQUE, confirmed INTEGER, deaths INTEGER, continent TEXT)''')
cur.execute('''CREATE TABLE Date
    (Date TEXT Unique)''')

# URL for scrapping data 
url = 'https://www.worldometers.info/coronavirus/countries-where-coronavirus-has-spread/'

# get URL html 


page = requests.get(url) 
soup = BeautifulSoup(page.text, 'html.parser') 


# soup.find_all('td') will find all element in the url's table with the <td> tag
data_iterator = iter(soup.find_all('td')) 
# data_iterator is the iterator of the table 

#Find the date of scraping to ensure that they are up to date
date = soup.find("div", attrs={"style":"font-size:13px; color:#999; text-align:center"})
date = date.text
date = date[14:]
cur.execute('INSERT or IGNORE into Date (Date) VALUES (?)', (date,))


# This loop will keep repeating till there is no more data available in the iterator 
while True: 
	try: 
		country = next(data_iterator).text 
		confirmed = next(data_iterator).text
		confirmed = int(confirmed.replace(',', '')) #convert to int
		deaths = next(data_iterator).text
		deaths = int(deaths.replace(',', '')) #convert to int
		continent = next(data_iterator).text 
        
		#cur.execute('SELECT id FROM Data')
		#row = cur.fetchone()
        
		cur.execute('INSERT or IGNORE into Data (country, confirmed, deaths, continent) VALUES (?, ?, ?, ?)', (country, confirmed, deaths, continent))
		conn.commit()
	# StopIteration error is raised when there are no more elements left to iterate through 
	except StopIteration: 
		break
	
print("Added Data into data.sqlite")
print("Data updated on:", date)

cur.close()
