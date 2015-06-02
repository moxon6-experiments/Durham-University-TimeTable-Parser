import requests
from requests.auth import HTTPBasicAuth
from project_exceptions import ResponseError
import os


def clear():
    print "\n \n \n"
    print "#"*20
    print "\n \n \n"
    os.system('cls')


def get_credentials():
    try:

        credentials = open(os.getenv('UserProfile') + "\\Desktop\\Sensitive\\sensitive.txt").read().splitlines()
    except IOError, e:
        print str(e)
        u = raw_input('Input username:')
        p = raw_input('Input password:')
        credentials = [u, p]
    return credentials


def get_days():
    """
    Returns a mapping of day number to day of week
    """
    return {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}


def get_auth_url(url, username=None, password=None):
    """
    Simple interface to query data from
    Basic  HTTP Authenticated Pages
    """
    print "Requesting"
    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    if response.ok:
        return response.content
    else:
        raise ResponseError(response.status_code)