from Handler import *
import re
import Database
import json
import logging

class CalendarHandler(Handler):
	def get(self):
		self.render('calendar.html')

class GetEventsHandler(Handler):
	def get(self):
		logging.info(self.get_query())
		self.response.write("""
[
  {
    "title": "All Day Event",
    "start": "2014-06-01"
  },
  {
    "title": "Long Event",
    "start": "2014-06-07",
    "end": "2014-06-10"
  },
  {
    "id": "999",
    "title": "Repeating Event",
    "start": "2014-06-09T16:00:00-05:00"
  },
  {
    "id": "999",
    "title": "Repeating Event",
    "start": "2014-06-16T16:00:00-05:00"
  },
  {
    "title": "Meeting",
    "start": "2014-06-12T10:30:00-05:00",
    "end": "2014-06-12T12:30:00-05:00"
  },
  {
    "title": "Lunch",
    "start": "2014-06-12T12:00:00-05:00"
  },
  {
    "title": "Birthday Party",
    "start": "2014-06-13T07:00:00-05:00"
  },
  {
    "title": "Click for Google",
    "url": "http://google.com/",
    "start": "2014-06-28"
  }
]
""")
