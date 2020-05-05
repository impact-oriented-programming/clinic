from datetime import datetime, timedelta, date
from datetime import datetime as dt
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
        events_per_day = events.filter(assigned = True ,date__day = day)
        d = ''
        my_day = day
        date_str = str(self.year) + str(self.month) + str(day)
        # print number of events when there is more than one event that day
        if len(events_per_day)>0:
            my_text = str({len(events_per_day)}) + 'scheduled appointments'
            d += f'<li> {events_per_day[0].get_html_url}</li>'
 
        if day != 0:
            if(date.today() == date(int(self.year), int(self.month), my_day)): # catch today to change it's background color
                return f"<td style='background: #8fb3cf; color:white;'><span class='date'>{day}</span><ul> {d} </ul></td>"
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
        events = gm.Appointment.objects.filter(date__year=self.year, date__month=self.month)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal