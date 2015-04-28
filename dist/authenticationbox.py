from Tkinter import Frame, Label, Button, Tk, Entry, W


class AuthenticationBox(Frame):
    def __init__(self):
        self.master = Tk()
        self.master.title('Log in to TimeTable Generator')
        self.entry_boxes = []
        for row, show, text in [(1, "", "CIS Username:"), (2, "*", "CIS Password")]:
            e = Entry(self.master, show=show, width=15)
            e.grid(row=row, column=1)
            Label(self.master, text=text).grid(row=row)
            self.entry_boxes.append(e)
        Button(self.master, text='Submit', command=self.quit).grid(row=3, column=1, sticky=W, pady=4)
        self.valid = False
        self.details = ["None"] * 2

    def mainloop(self):
        self.master.mainloop()

    def quit(self):
        self.details = [x.get() for x in self.entry_boxes]
        self.valid = True
        self.master.destroy()
