from Tkinter import Frame, OptionMenu, StringVar


class ModuleMenu(Frame):
    def __init__(self, master, module_dict):
        Frame.__init__(self, master)
        self.moduleDict = module_dict
        self.department = StringVar(self)
        self.module = StringVar(self)
        self.department.trace('w', self.update_options)
        keys = self.moduleDict.keys()
        keys.sort()
        self.departmentMenu = OptionMenu(self, self.department, *keys)
        self.moduleMenu = OptionMenu(self, self.module, '')
        self.department.set('None')

        self.departmentMenu.grid(row=1, column=1)
        self.moduleMenu.grid(row=1, column=2)
        self.pack()

    def update_options(self, *args):
        module_values = self.moduleDict[self.department.get()]
        self.module.set(module_values[0])
        menu = self.moduleMenu['menu']
        menu.delete(0, 'end')
        for module_value in module_values:
            menu.add_command(label=module_value)

    def get_module_code(self):
        return (self.module.get().split(' - '))[0]