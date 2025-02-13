import os
import requests
from icalendar import Calendar

# Step 1: Download the ICS file from the URL
url = "https://yangh9.github.io/ChinaCalendar/cal_lunar.ics"
response = requests.get(url)
ics_data = response.text

# Step 2: Parse the ICS data using icalendar
calendar = Calendar.from_ical(ics_data)

# Step 3: Modify each event
for component in calendar.walk('vevent'):
    # Get the current LOCATION and SUMMARY values
    location = component.get('LOCATION', '')
    summary = component.get('SUMMARY', '')
    
    if location:
        # Update SUMMARY to LOCATION value
        component['SUMMARY'] = f"『{location}』"
        # Remove LOCATION
        del component['LOCATION']

# Step 4: Save the modified ICS data to a new file
output_path = 'modified_cal_lunar.ics'

# Debug: print the current working directory
print(f"Current working directory: {os.getcwd()}")

with open(output_path, 'wb') as f:
    f.write(calendar.to_ical())

print(f"ICS file saved as {output_path}.")
