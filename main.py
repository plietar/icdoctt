from urllib.request import urlopen
import bs4 as BeautifulSoup
import requests
import re

WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

soup = BeautifulSoup.BeautifulSoup(requests.get('http://www.doc.ic.ac.uk/internal/timetables/2014-15/autumn/class/9_2_10.htm').text)
table = soup.find('table')
body = table.tbody

print(soup.find_all('h3')[1].get_text().strip())
print()

for tr in body.find_all('tr'):
    tds = [ [s for s in td.strings if not s.isspace()] for td in tr.find_all('td') ]

    time = int(tds[0][0][0:2])

    for i in range(1,6):
        if tds[i]:
            m = re.fullmatch(r'(\w{3}) \((\d+)-(\d+)\) / (.+)? / ?(.+)?', tds[i][1])

            print(tds[i][0])
            print('%s %dh - %dh' % (WEEKDAYS[i-1], time, time + 1))
            if m.group(1) != 'Wks':
                print(m.group(1))
            print('Weeks %d - %s' % (int(m.group(2)), int(m.group(3))))
            if m.group(4):
                print('%s' % m.group(4))
            if m.group(5):
                print('Room %s' % m.group(5))
            print()

