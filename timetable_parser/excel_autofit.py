from xlwings import *
import os


def auto_fit_columns(file_name):
    """
    Open an Excel Sheet and automatically
    adjust the column widths
    """
    wb = Workbook(r""+os.getcwd()+"\\"+file_name)
    num_sheets = Sheet.count()
    for x in range(1, num_sheets+1):
        Sheet(x).autofit()