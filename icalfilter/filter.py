import icalendar

def filter_ical(cal, rules):
    filtered_cal = icalendar.Calendar()

    for comp in cal.walk():
        match = True
        for key, regexes in rules.items():
            if key in comp:
                for regex in regexes:
                    match = match and regex.search(comp[key])
        if match:
            filtered_cal.add_component(comp)

    return filtered_cal
