from urllib.request import urlopen
import bs4 as BeautifulSoup
import requests
import re
import icalendar as ical
import datetime as dt
import sys
from pytz import timezone

if len(sys.argv) != 2:
    print("Usage : %s CLASS" % sys.argv[0], file=sys.stderr)
    sys.exit(1)

clazz = sys.argv[1]

termstart = dt.date(2014, 10, 6)

cal = ical.Calendar()

soup = BeautifulSoup.BeautifulSoup(requests.get('http://www.doc.ic.ac.uk/internal/timetables/2014-15/autumn/class/%s_1_1.htm' % clazz).text)
table = soup.find('table')
body = table.tbody

cal['summary'] = soup.find_all('h3')[1].get_text().strip()

print(soup.find_all('h3')[1].get_text().strip(), file=sys.stderr)
print(file=sys.stderr)

for tr in body.find_all('tr'):
    tds = [ [s for s in td.strings if not s.isspace()] for td in tr.find_all('td') ]

    time = dt.time(hour=int(tds[0][0][0:2]), tzinfo=timezone('Europe/London'))

    for i in range(5):
        td = tds[i + 1]
        if td:
            m = re.fullmatch(r'(\w{3}) \((\d+)-(\d+)\) / (.+)? / ?(.+)?', td[1])

            for w in range(int(m.group(2)), int(m.group(3)) + 1):
                t = dt.datetime.combine(termstart + dt.timedelta(weeks = (w - 1), days = i), time)
                
                print(td[0], file=sys.stderr)
                print(t, file=sys.stderr)

                if m.group(1) != 'Wks':
                    print(m.group(1), file=sys.stderr)
                if m.group(4):
                    print('%s' % m.group(4), file=sys.stderr)
                if m.group(5):
                    print('Room %s' % m.group(5), file=sys.stderr)
                print(file=sys.stderr)

                event = ical.Event()
                event.add('summary', td[0])
                event.add('dtstart', t)
                event.add('dtend', t + dt.timedelta(hours = 1))
                if m.group(5):
                    event['location'] = ical.vText('Room %s' % m.group(5))
                cal.add_component(event)
                
sys.stdout.buffer.write(cal.to_ical())

