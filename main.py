from urllib.request import urlopen
import bs4 as BeautifulSoup
import requests
import re
import datetime as dt

WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

termstart = dt.date(2014, 10, 6)

soup = BeautifulSoup.BeautifulSoup(requests.get('http://www.doc.ic.ac.uk/internal/timetables/2014-15/autumn/class/9_2_10.htm').text)
table = soup.find('table')
body = table.tbody

print(soup.find_all('h3')[1].get_text().strip())
print()

for tr in body.find_all('tr'):
    tds = [ [s for s in td.strings if not s.isspace()] for td in tr.find_all('td') ]

    time = dt.time(hour=int(tds[0][0][0:2]))

    for i in range(5):
        td = tds[i + 1]
        if td:
            m = re.fullmatch(r'(\w{3}) \((\d+)-(\d+)\) / (.+)? / ?(.+)?', td[1])

            for w in range(int(m.group(2)), int(m.group(3)) + 1):
                t = dt.datetime.combine(termstart + dt.timedelta(weeks = (w - 1), days = i), time)
                
                print(td[0])
                print(t)

                if m.group(1) != 'Wks':
                    print(m.group(1))
                if m.group(4):
                    print('%s' % m.group(4))
                if m.group(5):
                    print('Room %s' % m.group(5))
                print()

