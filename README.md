# Imperial College DoC Timetable
This is a parser for Imperial DoC's timetables found at http://www.doc.ic.ac.uk/internal/timetables/2014-15/autumn/class/.
It converts the html table to an iCal file.

## Usage
The converter has two modes, command-line and server modes.

### Command-line
Command-line mode fetches the timetable, converts it and prints it to stdout.

    ./icdoctt.py COURSE > calendar.ics

where COURSE is the course code (see below), such as `j1`.

### Server
Server mode starts a tiny http server. The converted calendar is available at `http://host:port/COURSE.ics` where COURSE is the course code (see below).

    ./icdoctt.py --server

You can also specify an interface to bind, and a port to listen to

    ./icdoctt.py --server 0.0.0.0:8080
    ./icdoctt.py --server :8080

You should now subscribe to the calendar in your calendaring software.

## Course Code
The converter uses a "course code" to identify which course's timetable should be retrieved.
You can find the course code at http://www.doc.ic.ac.uk/internal/timetables/2014-15/autumn/class/.

It is written at the right of the course's name. For example JMC 1's code is j1.
