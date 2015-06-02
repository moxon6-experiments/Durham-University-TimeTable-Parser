from Tkinter import *
import createsheet
from getmodules import get_module_dict
from authenticationbox import AuthenticationBox
from module_menu import ModuleMenu

"""
Root module for TimeTable Parser GUI
"""


class ModuleWindow(Frame):
    def __init__(self, module_dict, details):
        self.master = Tk()
        self.master.title('Module Master')
        self.module_dict = module_dict
        self.details = details
        self.moduleBoxes = [ModuleMenu(self.master, self.module_dict) for x in range(0, 6)]
        self.button = Button(self.master, text='Submit', command=self.timetable)
        self.button.pack()

    def timetable(self):
        module_list = [x.module.get().split(" - ")[0] for x in self.moduleBoxes if x.module.get() != ""]
        self.master.withdraw()
        createsheet.create_timetable(module_list, self.details)
        self.master.destroy()

    def mainloop(self, n=0):
        self.master.mainloop()


def main():
    auth_box = AuthenticationBox()
    auth_box.mainloop()
    module_dict = get_module_dict(*auth_box.details)
    module_window = ModuleWindow(module_dict, auth_box.details)
    module_window.mainloop()


def test():
    from utils import get_credentials
    credentials = get_credentials()
    module_dict = get_module_dict(*credentials)
    module_window = ModuleWindow(module_dict, credentials)
    module_window.mainloop()


if __name__ == "__main__":
    # main()
    test()
