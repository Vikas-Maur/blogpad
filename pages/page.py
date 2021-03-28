from tkinter import *

class Page(Frame):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)

        # Preventing the frame to adjust according to the child size
        self.grid_propagate(0)
        self.pack_propagate(0)

        self.master = master

        self.shortcuts = {}

    def ActivatePage(self):
        for key,value in self.shortcuts.items():
            self.master.bind(key,value)

    def DeActivatePage(self):
        for key in self.shortcuts.keys():
            self.master.unbind(key)
