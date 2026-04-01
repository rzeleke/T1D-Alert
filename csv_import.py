#Import libraries
import re # text pattern
from datetime import datetime, timedelta # 

# Exercise events - Keyword List
EXERCISE_KEYWORDS = [
    'gym', 'run', 'workout', 'soccer', 'swim',
    'practice', 'exercise', 'yoga', 'bike', 'walk',
    'tennis', 'basketball', 'football', 'training'
]

# Function to check if an event is exercise-related
def parse_calendar_datetime(date_string):
    # Remove leading/trailing whitespace
    date_string = date_string.strip()     
    # checks if this is a timed event or an all-day event               
    try:
        if 'T' in date_string:   
            return datetime.strptime(date_string.replace('Z', ''), '%Y%m%dT%H%M%S')
        else:
            return datetime.strptime(date_string, '%Y%m%d')  
    #If something goes wrong, return None instead of crashing 
    except ValueError:
        return None

#Read each calender event and check if it contains any exercise-related keywords
def parse_exercise_event(filepath):
    completed_events = [] 
    current_event = {}  

    #Opening the file and loop through it line by line
    with open(filepath, 'r', encoding='utf-8') as calendar_file: 
        for line in calendar_file: 
            line = line.strip() 
            if line.startswith('BEGIN:VEVENT'):
                current_event = {} 

            elif line.startswith('END:VEVENT'):
                if current_event:
                    completed_events.append(current_event)
                current_event = {}
                
            elif line.startswith('SUMMARY:'):
                current_event['title'] = line[len('SUMMARY:'):]

            #extract just the date part of the start and end times, ignoring the time component    
            elif line.startswith('DTSTART'):
                value = line.split(':', 1)[-1]
                current_event['start'] = parse_calendar_datetime(value)

            elif line.startswith('DTEND'):
                value = line.split(':', 1)[-1]
                current_event['end'] = parse_calendar_datetime(value)

            elif line.startswith('DESCRIPTION:'):
                current_event['description'] = line[len('DESCRIPTION:'):]
    return completed_events

# Check if an event title contains an exercise keyword
def is_exercise_event(title):
    #Convert the title to lowercase. This makes the search case-insensitive
    title_lower = title.lower()
    return any(keyword in title_lower for keyword in EXERCISE_KEYWORDS)

#This function takes the full list of all events and returns only the exercise ones
def filter_exercise_events(calendar_events):
    exercise_events = []
    #Loops through every event in the list one at a time
    for event in calendar_events:
        #Gets the title from the event dictionary
        title = event.get('title', '')
        if is_exercise_event(title):
            exercise_events.append(event)
    return exercise_events
# reads the calendar file and returns exercise events
def get_exercise_events(filepath):
    #read all events from the file
    calendar_events = parse_exercise_event(filepath)
    #filter to exercise events only
    exercise_events = filter_exercise_events(calendar_events)
    return calendar_events, exercise_events

# Test block - only runs when this file is executed directly
if __name__ == '__main__':
    all_events, exercise_events = get_exercise_events('sample_calendar.ics')

    print(f"Total events found:    {len(all_events)}")
    print(f"Exercise events found: {len(exercise_events)}")
    print()

    for event in exercise_events:
        print(f"  Title : {event['title']}")
        print(f"  Start : {event['start']}")
        print(f"  End   : {event['end']}")
        print()


