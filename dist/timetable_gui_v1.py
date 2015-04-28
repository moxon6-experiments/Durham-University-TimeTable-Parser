from Tkinter import *
from createsheet import create_timetable
from getmodules import get_module_dict


class AuthenticationBox():
    def __init__(self):
        self.master = Tk()
        self.master.title('Log in to TimeTable Generator')
        self.entry_boxes = []
        for row, show, text in [(1, "", "CIS Username:"), (2, "*", "CIS Password:")]:
            e = Entry(self.master, show=show, width=15)
            e.grid(row=row, column=1)
            Label(self.master, text=text).grid(row=row)
            self.entry_boxes.append(e)
        Button(self.master, text='Submit', command=self.quit).grid(row=3, column=1, sticky=W, pady=4)
        self.valid = False
        self.details = ["null", "null"]

    def mainloop(self):
        self.master.mainloop()

    def quit(self):
        self.details = [x.get() for x in self.entry_boxes]
        self.valid = True
        self.master.destroy()

    def get_details(self):
        return self.details


class ModuleSelection(Frame):
    def __init__(self, username, password):
        self.master = Tk()
        self.master.title('Module Master')
        self.module_list = ['None'] * 6
        self.moduleDict = get_module_dict(username, password)
        self.module_boxes = [ModuleMenu(self.master, self.moduleDict) for x in range(0, 6)]
        self.button = Button(self.master, text='Submit', command=self.quit)
        self.button.pack()
        self.pack()

    def mainloop(self):
        self.master.mainloop()

    def quit(self):
        self.module_list = [x.module.get().split(" - ")[0] for x in self.module_boxes if x.module.get() != ""]
        self.master.destroy()


class ModuleDropDown(Frame):
    def __init__(self, master, module_dict):
        self.master = master
        self.moduleDict = module_dict
        self.department = StringVar()
        self.module = StringVar()
        self.department.trace('w', self.update_options)
        keys = self.moduleDict.keys()
        keys.sort()
        self.departmentMenu = OptionMenu(self.master, self.department, *keys)
        self.moduleMenu = OptionMenu(self.master, self.module, '')
        self.department.set('None')
        self.departmentMenu.grid(row=1, column=1)
        self.moduleMenu.grid(row=1, column=2)
        self.pack()

    def update_options(self):
        module_values = self.moduleDict[self.department.get()]
        self.module.set(module_values[0])
        menu = self.moduleMenu['menu']
        menu.delete(0, 'end')
        for moduleValue in module_values:
            menu.add_command(label=moduleValue, command=lambda module_value: self.module.set(module_value))

###
class ModuleMenu2(Frame):
    def __init__(self, master, moduleDict):
        Frame.__init__(self, master)
        self.moduleDict = moduleDict
        self.department = StringVar(self)
        self.module = StringVar(self)
        self.department.trace('w', self.updateoptions)
        keys = self.moduleDict.keys()
        keys.sort()
        self.departmentMenu = OptionMenu(self, self.department, *keys)
        self.moduleMenu = OptionMenu(self.master, self.module, '')
        self.department.set('None')

        #self.departmentMenu.pack()
        #self.moduleMenu.pack()
        self.departmentMenu.grid(row=1, column=1)
        self.moduleMenu.grid(row=1, column=2)
        self.pack()
    def updateoptions(self, *args):
        moduleValues = self.moduleDict[self.department.get()]
        self.module.set(moduleValues[0])
        menu = self.moduleMenu['menu']
        menu.delete(0, 'end')
        for moduleValue in moduleValues:
            menu.add_command(label=moduleValue, command=lambda moduleValue=moduleValue: self.module.set(moduleValue))
    def getModuleCode(self):
        return (self.module.get().split(' - '))[0]
####


def main():
    """
    Main module function
    """
    auth_box = AuthenticationBox()
    auth_box.mainloop()

    if auth_box.valid:
        module_selection = ModuleSelection(auth_box.get_details()[0], auth_box.get_details()[1])
        module_selection.mainloop()
        create_timetable(module_selection.module_list, auth_box.details)


def test():
    from utils import get_credentials
    credentials = get_credentials()
    module_selection = ModuleSelection(*credentials)
    module_selection.mainloop()


if __name__ == "__main__":
    # main()
    test()
