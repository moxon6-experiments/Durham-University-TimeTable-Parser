from bs4 import BeautifulSoup
import re
from utils import get_auth_url, get_days
from scheduleitem import ScheduleItem


def get_table_raw(page_raw):
    """
    String page_raw -> Relevant Section String page_raw
    Takes a String of a full HTML page, and outputs the substring
    appearing between '<!-- START ROW OUTPUT -->' and '<!-- END ROW OUTPUT -->'
    """
    start = '<!-- START ROW OUTPUT -->'
    row_start = page_raw.find(start)
    end = '<!-- END ROW OUTPUT -->'
    row_end = page_raw.find(end)
    page_raw = page_raw[row_start + len(start):row_end]
    return page_raw


def parse_row(table_row, module_list):
    """
    BeautifulSoup table_row, List module_list -> List schedule_items
    Iterates through a row of
    """
    schedule_items = []
    day = 1.0  # Monday
    time = 9.0  # 9 a.m
    for row_item in table_row:
        if 'colspan' in row_item.attrs:
            time_block = int(row_item.attrs['colspan']) / 4
            new_item = ScheduleItem(day, time, time_block, row_item, module_list)
            schedule_items.append(new_item)
        else:
            time_block = 0.25
        time += time_block
        if time >= 18.25:  # If time is after 6:15 pm
            time -= 9.25  # Time is actually the start of the next day
            day += 1  # So increment the day
    return schedule_items


def get_table_rows(table_raw):
    """
    Takes a String of Raw html and converts it to a list of BeautifulSoup td objects
    """
    table_content = BeautifulSoup(table_raw)
    table_trs = table_content.findAll('tr', recursive=False)
    table_tds = [y.findAll('td', recursive=False) for y in table_trs]
    for row_index in range(len(table_tds)):
        if table_tds[row_index][0].string is None:
            continue
        elif re.match("[A-Za-z]{4}[0-9]{4}", table_tds[row_index][0].string.encode('ASCII', 'ignore')) is not None:
            table_tds[row_index] = table_tds[row_index][1:]
    return table_tds


def parse_timetable_data(page_html, module_list):
    """
    String page_html, List module_list  -> List of Schedule Items

    Takes a raw html string, and a list of modules
    and returns a list of ScheduleItems defined by that html string
    """
    table_raw = get_table_raw(page_html)
    table_rows = get_table_rows(table_raw)
    schedule_items = []
    for table_row in table_rows:
        schedule_items += parse_row(table_row, module_list)
    return list(set(schedule_items))


def get_url_from_modules(module_list):
    """
    Takes a list of module codes
        e.g. ["MATH1234","COMP1234"]
    and generates a url from which to pull
    timetable data and returns this url
    """
    if len(module_list) == 1:
        module_list *= 2
    module_string = ""
    for module_code in module_list:
        module_string += (module_code + "%0D%0A")
    url = ("http://timetable.dur.ac.uk/reporting/master;module;name;%s?days=1-5&weeks=11-47"
           + "&periods=5-41&template=module+master"
           + "&height=100&week=100") % module_string
    return url


def get_schedule_items(module_list, details):
    """
    List module_list, tuple(username,password) -> List of Schedule Items
    """
    url = get_url_from_modules(module_list)
    page_data = get_auth_url(url, details[0], details[1])
    schedule_items = parse_timetable_data(page_data, module_list)
    return schedule_items