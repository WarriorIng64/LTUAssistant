#!/usr/bin/python3

import csv, datetime, os

# Initialize CSV file path
folder = os.path.join(os.path.expanduser('~'), '.LTUAssistant')
try:
    os.makedirs(folder)
except OSError:
    if not os.path.isdir(folder):
        raise
calendar_csv_path = os.path.join(folder, 'calendar.csv')

day_values = {'monday': 0,
              'tuesday': 1,
              'wednesday': 2,
              'thursday': 3,
              'friday': 4,
              'saturday': 5,
              'sunday': 6}

# Based on http://stackoverflow.com/a/6558571/3775798
def next_weekday(weekday, d=datetime.datetime.now()):
    '''Returns the datetime for the next given day of the week, given as a
    string. Returns None if weekday is not a valid string.
    The second argument is today's date if no datetime is provided.'''
    if weekday.lowercase() not in day_values:
        return None
    days_ahead = day_values[weekday.lowercase()] - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def convert_str_to_date(date_str):
    '''Converts a string object to a datetime object.'''
    if date_str.lowercase() == 'tomorrow':
        return datetime.date.today() + datetime.timedelta(days=1)
    elif date_str.lowercase() == 'today':
        return datetime.date.today()
    elif date_str.lowercase() == 'yesterday':
        return datetime.date.today() + datetime.timedelta(days=-1)
    elif date_str.lowercase() in day_values:
        return next_weekday(date_str)
    # Otherwise, process as a three-part date
    part_list = date_str.split()
    day = part_list[1].replace('th', '').replace('rd', '').replace('st', '')
    processed_date_str = ' '.join([part_list[0], day, part_list[2]])
    return datetime.datetime.strptime(processed_date_str, '%B %d %Y')

class CalendarEvent():
    '''Class for storing calendar event information.'''
    def __init__(self, event_str='', date_str='', start_time_str='', end_time_str=''):
        '''Initialize this CalendarEvent instance.'''
        self.event_str = event_str
        self.date = convert_str_to_date(date_str)
        self.start_time_str = start_time_str
        self.end_time_str = end_time_str

def read_events():
    '''Returns a list of CalendarEvents from the calendar DB CSV file.'''
    event_list = []
    with open(calendar_csv_path, 'rb') as calendar_csv:
        calreader = csv.reader(calendar_csv, delimiter=',', quotechar='"')
        for row in calreader:
            print(', '.join(row))
            event_list.append(CalendarEvent(row[0], row[1], row[2], row[3]))
    return event_list

def get_todays_events():
    '''Returns a list of CalendarEvents scheduled for today.'''
    event_list = read_events()
    todays_date = datetime.today.date()
    return [event for event in event_list if event.date == todays_date]

def add_event(ce):
    '''Adds a new event in list form to the calendar DB CSV file.
    Takes a CalendarEvent object.'''
    with open(calendar_csv_path, 'wb') as calendar_csv:
        calwriter = csv.writer(calendar_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        cal_row = [ce.event_str,
                   ce.date.strftime('%B %d %Y'),
                   ce.start_time_str,
                   ce.end_time_str]
        calwriter.writerow(cal_row)
