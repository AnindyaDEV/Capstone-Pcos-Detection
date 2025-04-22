from flask import Blueprint, render_template, request, make_response
from datetime import datetime, timedelta
import math, icalendar

menstrual_routes = Blueprint("menstrual_routes", __name__)

@menstrual_routes.route("/menstrual_tracker", methods=["POST"])
def menstrual_tracker():
    last_period_str = request.form["last_period"]
    period_length = int(request.form["period_length"])
    cycle_length = int(request.form["cycle_length"])
    last_period_date = datetime.strptime(last_period_str, "%Y-%m-%d")

    events = []

    start_year, end_year = 2001, 2100
    years_before = (last_period_date.year - start_year)
    cycles_before = math.ceil((years_before * 365) / cycle_length) + 1
    years_after = (end_year - last_period_date.year)
    cycles_after = math.ceil((years_after * 365) / cycle_length) + 1

    for cycle in range(-cycles_before, cycles_after + 1):
        cycle_start = last_period_date + timedelta(days=cycle * cycle_length)
        if not (start_year <= cycle_start.year <= end_year): continue

        for i in range(period_length):
            day = cycle_start + timedelta(days=i)
            events.append({"title": "Period Day", "start": day.strftime("%Y-%m-%d"), "color": "#ff6b81"})

        for i in range(1, 3):
            day = cycle_start - timedelta(days=i)
            events.append({"title": "Pre-Period", "start": day.strftime("%Y-%m-%d"), "color": "#feca57"})

        for i in range(period_length, period_length + 2):
            day = cycle_start + timedelta(days=i)
            events.append({"title": "Post-Period", "start": day.strftime("%Y-%m-%d"), "color": "#7ed6df"})

        ovulation_day = cycle_start + timedelta(days=cycle_length - 16)
        fertile_start = ovulation_day - timedelta(days=3)
        fertile_end = ovulation_day + timedelta(days=1)

        current_day = fertile_start
        while current_day <= fertile_end:
            events.append({"title": "Fertile Window", "start": current_day.strftime("%Y-%m-%d"), "color": "#badc58"})
            current_day += timedelta(days=1)

        events.append({"title": "Ovulation", "start": ovulation_day.strftime("%Y-%m-%d"), "color": "#e056fd"})

    return render_template("menstrual_tracker.html", events=events, last_period=last_period_str,
                           period_length=period_length, cycle_length=cycle_length)


@menstrual_routes.route("/download_ical", methods=["POST"])
def download_ical():
    last_period_str = request.form["last_period"]
    period_length = int(request.form["period_length"])
    cycle_length = int(request.form["cycle_length"])
    last_period_date = datetime.strptime(last_period_str, "%Y-%m-%d")

    cal = icalendar.Calendar()
    cal.add('prodid', '-//Harmony Menstrual Tracker//')
    cal.add('version', '2.0')

    start_year, end_year = 2001, 2100
    years_before = (last_period_date.year - start_year)
    cycles_before = math.ceil((years_before * 365) / cycle_length) + 1
    years_after = (end_year - last_period_date.year)
    cycles_after = math.ceil((years_after * 365) / cycle_length) + 1

    for cycle in range(-cycles_before, cycles_after + 1):
        cycle_start = last_period_date + timedelta(days=cycle * cycle_length)
        if not (start_year <= cycle_start.year <= end_year): continue

        period_end = cycle_start + timedelta(days=period_length - 1)
        event = icalendar.Event()
        event.add('summary', 'Period')
        event.add('dtstart', cycle_start.date())
        event.add('dtend', (period_end + timedelta(days=1)).date())
        cal.add_component(event)

        ovulation_day = cycle_start + timedelta(days=cycle_length - 16)
        event = icalendar.Event()
        event.add('summary', 'Ovulation')
        event.add('dtstart', ovulation_day.date())
        event.add('dtend', (ovulation_day + timedelta(days=1)).date())
        cal.add_component(event)

        fertile_start = ovulation_day - timedelta(days=3)
        fertile_end = ovulation_day + timedelta(days=1)
        event = icalendar.Event()
        event.add('summary', 'Fertile Window')
        event.add('dtstart', fertile_start.date())
        event.add('dtend', (fertile_end + timedelta(days=1)).date())
        cal.add_component(event)

    response = make_response(cal.to_ical())
    response.headers['Content-Type'] = 'text/calendar'
    response.headers['Content-Disposition'] = 'attachment; filename=menstrual_calendar.ics'
    return response
