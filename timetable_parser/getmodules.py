import re
from bs4 import BeautifulSoup
from utils import get_auth_url


def get_module_page_html(username, password):
    url = "https://timetable.dur.ac.uk/module.htm"
    return get_auth_url(url, username, password)


def get_module_dict(username, password):
    """
    Logs in to Durham TimeTable site nad pulls a list of available modules
    """
    page_html = get_module_page_html(username, password)
    page_html = page_html.split('<select style=\'width:450px\' name=\'identifier\' size=\'5\' multiple>')[1]
    page_html = page_html.split('</select>')[0]
    page_content = BeautifulSoup(page_html)
    options = page_content.findAll('option', recursive=False)
    modules = {}
    for option in options:
        module_code = option.attrs['value'].encode('ASCII', 'ignore')
        module_code = re.sub('[^A-Za-z]', "", module_code)
        module_code = (module_code+"    ")[0:4].replace(" ", "")
        if module_code not in modules:
            modules[module_code] = [option.contents[0].encode('ASCII', 'ignore')]
        else:
            modules[module_code].append(option.contents[0].encode('ASCII', 'ignore'))
    modules['None'] = ['']
    return modules