"""
-------------------------------------------------------------------------------
 Name:        ex
 Purpose:     Small Module containing custom exceptions

 Author:      Martin Moxon

 Created:     25/04/2015
 Copyright:   (c) Martin 2015
 Licence:     <your licence>
-------------------------------------------------------------------------------
"""


class ResponseError(Exception):
    """
    Custom exception for querying sites with Basic HTTP Authentication
    Provides a status code when raised
    """
    def __init__(self, status_code):
        Exception.__init__(self)
        self.status_code = status_code
        status_dict = {
            404: "404: Page Not Found",
            401: "401: Invalid Username/Password Combination Entered"
            }
        if status_code in status_dict:
            self.message = status_dict[status_code]
        else:
            self.message = "%d: An Error Occurred Querying Remote Server" % self.status_code

    def __str__(self):
        return self.message
