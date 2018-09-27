'''
import pandas as pd
from bs4 import BeautifulSoup
import requests

def get_companies():
    url = 'http://edgarpulse.com/api/v1/insidertrades/filings'
    # url = 'http://api.corpwatch.org/2008/companies.json?sic_code='+str(sic_code)
    response = requests.get(url)
    page = response.content
    soup = BeautifulSoup(page, 'lxml')

    html = list(soup.children)[0]

    # print html

    body = list(html.children)[0]


    a = list(body.children)[0]
    print a
#
get_companies()
'''

'''
import datetime

current_year = datetime.date.today().year
current_quarter = (datetime.date.today().month - 1) // 3 + 1
start_year = 2018
years = list(range(start_year, current_year))
quarters = ['QTR1', 'QTR2', 'QTR3', 'QTR4']
history = [(y, q) for y in years for q in quarters]
for i in range(1, current_quarter + 1):
    history.append((current_year, 'QTR%d' % i))
urls = ['https://www.sec.gov/Archives/edgar/full-index/%d/%s/master.idx' % (x[0], x[1]) for x in history]
urls.sort()

# Download index files and write content into SQLite
import sqlite3
import requests

con = sqlite3.connect('edgar_idx.db')
cur = con.cursor()
cur.execute('DROP TABLE IF EXISTS idx')
cur.execute('CREATE TABLE idx (cik TEXT, conm TEXT, type TEXT, date TEXT, path TEXT)')

for url in urls:
    lines = requests.get(url).text.splitlines()
    records = [tuple(line.split('|')) for line in lines[11:]]
    cur.executemany('INSERT INTO idx VALUES (?, ?, ?, ?, ?)', records)
    print(url, 'downloaded and wrote to SQLite')

con.commit()
con.close()

# Write SQLite database to Stata
import pandas
from sqlalchemy import create_engine

engine = create_engine('sqlite:///edgar_idx.db')
with engine.connect() as conn, conn.begin():
    data = pandas.read_sql_table('idx', conn)
    j = data.to_json('edgar_idx.json')

'''
import requests
import pandas as pd
from bs4 import BeautifulSoup

url='https://www.sec.gov/Archives/edgar/full-index/2018/QTR1/master.idx'
lines = requests.get(url).text.splitlines()

records = []
for line in range(11,len(lines)):

    records.append(lines[line])

paths_list=[]
for record in range(len(records)):
    paths_list.append(records[record].split('|'))

path = []
for i in range(len(paths_list)):
    path.append(str('https://www.sec.gov/Archives/')+paths_list[i][-1])

for url in range(len(path)):
    soup = BeautifulSoup(requests.get(path[url]).text)
