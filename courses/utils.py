from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Lesson


class Calendar(HTMLCalendar):

    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, lessons):
        lessons_per_day = lessons.filter(date_time__day=day)
        d = ''
        for lesson in lessons_per_day:
            d += f'<li class="calendar_list"> {lesson.get_html_url} </li>'
        if day != 0:
            return f"<td class='date_cell'>{day}<ul>{d}</ul></td>"
        return "<td class='date_cell'><ul></ul></td>"

    def formatweek(self, theweek, lessons):
        week = ""
        for d, weekday in theweek:
            week += self.formatday(d, lessons)
        return f'<tr> {week} </tr>'

    def formatmonth(self):
        lessons = Lesson.objects.filter(date_time__year=self.year, date_time__month=self.month)
        cal = f'<table class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=True)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, lessons)}\n'
        return cal
