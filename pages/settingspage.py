from tkinter import *
from tkinter import ttk,filedialog
from . import page
from .utils import MyButton,COLORS
import os

class SettingPage(page.Page):
    def __init__(self,master,info,**kwargs):
        super().__init__(master,**kwargs)

        self.info = info
        self.background = "lightgrey"
        self.config(background=self.background)

        self.master_shortcuts = {"<Control-s>":lambda e:self.UpdateInfo,"<Control-c>":lambda e:self.master.GoToPrevPage}

        self.setting_frame = Frame(self,bg=self.background)
        self.setting_frame.pack(pady=(50,0))

        self.row = 0
        self.db_entries = self.CreateDatabaseSettings()
        self.choose_dir = MyButton(self.setting_frame,color="lightgrey",font=self.font, text="Choose Dir",
                                 command=self.ChooseDir)
        self.choose_dir.grid(row=self.row, column=2, sticky="nsew")
        self.save_file_entry = self.CreateEntry("Default Dir To Save File",os.path.relpath(self.info["saved_file_dir"]))

        self.cancel_button = MyButton(self.setting_frame,color=COLORS["warning"],font=self.font,text="Cancel(ctrl+c)"
                                      ,bg=COLORS["danger"],fg="white"
                                      ,command=self.master.GoToPrevPage)
        self.cancel_button.grid(row=self.row,column=0,sticky="nsew",pady=20,padx=10)

        self.save_button = MyButton(self.setting_frame,color=COLORS["primary"],font=self.font,text="Save(ctrl+s)"
                                    ,bg=COLORS["success"],fg="white"
                                    ,command=self.UpdateInfo)
        self.save_button.grid(row=self.row,column=1,sticky="nsew",pady=20,padx=10)

    def CreateDatabaseSettings(self):
        info = self.info["database"]
        entries = {}
        for key,value in info.items():
            e=self.CreateEntry(key,value)
            entries[key]=e
        return entries

    def CreateEntry(self,text,value):
        config = {"bg": self.background, "font": self.font}
        l = Label(self.setting_frame,text=text.upper()+":",**config)
        l.grid(row=self.row,column=0)
        e = ttk.Entry(self.setting_frame,font=self.font)
        e.grid(row=self.row, column=1, sticky="nsew", pady=10, padx=10)
        e.insert("0", value)
        self.row+=1
        return e

    def UpdateInfo(self):
        for key in self.info["database"].keys():
            self.info["database"][key] = self.db_entries[key].get()
        self.info["saved_file_dir"]= os.path.abspath(self.save_file_entry.get())
        self.master.UpdateDBInfo(self.info)

    def ChooseDir(self):
        dir = filedialog.askdirectory()
        if dir:
            dir = os.path.relpath(dir)
            self.save_file_entry.delete("0","end")
            self.save_file_entry.insert("0",dir)
