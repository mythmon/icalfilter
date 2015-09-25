import re

import icalendar
import requests
from flask import Flask, request, Response

from icalfilter.filter import filter_ical

app = Flask(__name__)

@app.route('/filter')
def filter():
    if 'calendar' not in request.args:
        return Response('calendar is a require arg', status=400)

    calendar_url = request.args['calendar']
    rules = make_rules(request.args.items())

    if not rules:
        return Response('rules are required', status=400)

    cal_text = requests.get(calendar_url).text

    try:
        cal = icalendar.Calendar.from_ical(cal_text)
    except ValueError:
        return Response('Could not parse ics file.', status=400)

    filtered_cal = filter_ical(cal, rules)
    return filtered_cal.to_ical()

def make_rules(raw_dict):
    rules = {}
    key_re = re.compile('^rule_(?:\d+_)?(.*)$')
    for key, val in raw_dict:
        match = key_re.match(key)
        if match:
            rule_name = match.group(1)
            rule_re = re.compile(val)
            rules.setdefault(rule_name, []).append(rule_re)
    return rules



if __name__ == '__main__':
    app.run(debug=True)
