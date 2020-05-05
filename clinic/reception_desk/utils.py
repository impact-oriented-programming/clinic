from datetime import datetime, timedelta
from calendar import HTMLCalendar
import general_models.models as gm
import datetime
from django.utils import timezone

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()
        self.setfirstweekday(6)
        
    # formats a day as a td
    # filter events by day
    def formatday(self, day, events):
        events_per_day = events.filter(date__day = day)
        d = ''
        # print number of events when there is more than one event that day
        if len(events_per_day)>0:
            d +=f'<li>  {len(events_per_day)} appointments</li>'
        #print all patient's names for that day - currently deleted
        #for event in events_per_day:
         #   d += f'<a> {event.patient} </a>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'
    # formats a week as a tr
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'
    
    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        events = gm.Appointment.objects.filter(assigned = True, date__year=self.year, date__month=self.month)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal