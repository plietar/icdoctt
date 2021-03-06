#!/usr/bin/env python3

import urllib.parse
import bs4 as BeautifulSoup
import requests
import re
import icalendar as ical
import datetime as dt
import sys
from pytz import timezone

TERMSTART = dt.date(2014, 10, 6)
COURSEMAP = {
        'c1': 1, 'c2':  2, 'c3':  3, 'c4':  4,
        'i1': 5, 'i2':  6, 'i3':  7, 'i4':  8,
        'j1': 9, 'j2': 10, 'j3': 11, 'j4': 12,
        'e3': 18, 'e4': 15,
        'hipeds': 30,
        'mres5': 28,
        'a5': 14,
        's5': 29,
        'i5': 17,
        'v5': 13
}

def get_timetable(cal, course, period):
    soup = BeautifulSoup.BeautifulSoup(requests.get('http://www.doc.ic.ac.uk/internal/timetables/2014-15/autumn/class/%s_%s.htm' % (course, period)).text)
    table = soup.find('table')
    body = table.tbody

    cal['summary'] = soup.find_all('h3')[1].get_text().strip()

    for tr in body.find_all('tr'):
        tds = [ [s for s in td.strings if not s.isspace()] for td in tr.find_all('td') ]

        time = dt.time(hour=int(tds[0][0][0:2]), tzinfo=timezone('Europe/London'))

        for i in range(5):
            td = tds[i + 1]
            if td:
                for j in range(0, len(td), 2):
                    r = td[j:j+2]

                    m = re.fullmatch(r'(\w{3}(/\w{3})?) \((\d+)-(\d+)\) / (.+)? / ?(.+)?', r[1])

                    for w in range(int(m.group(3)), int(m.group(4)) + 1):
                        t = dt.datetime.combine(TERMSTART + dt.timedelta(weeks = (w - 1), days = i), time)

                        event = ical.Event()
                        event.add('summary', r[0])
                        event.add('dtstart', t)
                        event.add('dtend', t + dt.timedelta(hours = 1))
                        if m.group(6):
                            event['location'] = ical.vText('Room %s' % m.group(6))
                        cal.add_component(event)

def get_data(course):
    course = COURSEMAP[course]
    cal = ical.Calendar()

    get_timetable(cal, course, '1_1')
    get_timetable(cal, course, '2_10')
    get_timetable(cal, course, '11_11')

    return cal.to_ical()


def main(course):
    sys.stdout.buffer.write(get_data(course))

def server(listen):
    from flask import Flask
    app = Flask(__name__)

    @app.route("/<course>.ics")
    def run(course):
        return get_data(course)

    if listen:
        host, port = urllib.parse.splitport(listen)
        app.run(host, int(port) if port is not None else None)
    else:
        app.run()

def usage():
    print("Usage : %s COURSE" % sys.argv[0], file=sys.stderr)
    print("        %s --server [LISTEN]" % sys.argv[0], file=sys.stderr)
    sys.exit(1)

if (len(sys.argv) == 2 or len(sys.argv) == 3) and sys.argv[1] == '--server':
    server(sys.argv[2] if len(sys.argv) == 3 else None)
elif len(sys.argv) == 2 and sys.argv[1] != '--server':
    main(sys.argv[1])
else:
    usage()


