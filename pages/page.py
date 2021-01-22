from tkinter import *

class Page(Frame):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)

        self.master = master

        self.font="consolas 20 bold"

        self.config(width=1300,height=700)

        self.pack_propagate(0)
        self.grid_propagate(0)

        self.master_shortcuts = {}

    def ActivatePage(self):
        for key,command in self.master_shortcuts.items():
            self.master.bind(key,func=command)

    def DeactivatePage(self):
        for key in self.master_shortcuts.keys():
            self.master.unbind(key)
