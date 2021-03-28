from .page import *
from tkinter import ttk,filedialog,messagebox
from pages.utils import *
import os

class SettingPage(Page):
    def __init__(self,master,first_time=False,**kwargs):
        super().__init__(master,**kwargs)

        self.name_label = Label(self,text="Change Settings",font="consolas 45 bold",bg="lightgrey")
        self.name_label.pack(side=TOP,pady=20,fill=X)

        self.info = self.master.info

        self.setting_frame = Frame(self)
        self.setting_frame.pack(side=TOP,pady=30)
        
        self.row = 0

        self.choose_dir_buttons = {}
        self.labels , self.entries = self.CreateSettings(self.info)

        if not first_time:
            self.cancel_button = HoverableButton(self.setting_frame
                                        ,on_enter={"background":COLORS["warning"]}
                                        ,background=COLORS["danger"]
                                        ,foreground="white"
                                        ,font="consolas 20 bold"
                                        ,text="Cancel Or Reset"
                                        ,command=self.Cancel
                                        )
            self.cancel_button.grid(row=self.row,column=0,sticky="nsew",padx=10,pady=10)
        
        self.save_button = HoverableButton(self.setting_frame
                                        ,on_enter={"background":"darkgreen"}
                                        ,background=COLORS["success"]
                                        ,foreground="white"
                                        ,font="consolas 20 bold"
                                        ,text="Save Settings"
                                        ,command=self.SaveSettings
                                        )
        self.save_button.grid(row=self.row,column=1,sticky="nsew",padx=10,pady=10)
        
        self.row+=1

    def CreateSettings(self,info):
        labels = {}
        entries = {}
        column = 0
        for key,value in info.items():
            if type(value)!=dict:
                labels[key] = Label(self.setting_frame,text=key,font="consolas 20 bold")
                entries[key] = ttk.Entry(self.setting_frame,font="consolas 20 bold")
                labels[key].grid(row=self.row,column=column,sticky="nsew",padx=10,pady=10)
                entries[key].grid(row=self.row,column=column+1,sticky="nsew",padx=10,pady=10)

                if type(value)==list:
                    self.choose_dir_buttons[key] = ttk.Button(self.setting_frame
                                                        ,text="Choose Dir"
                                                        ,command=lambda entry=entries[key]:self.ChooseFolder(entry)
                                                        )
                    self.choose_dir_buttons[key].grid(row=self.row,column=column+2,sticky="nsew",padx=10,pady=10)
                    entries[key].insert('0',os.path.relpath(value[0]))
                else:
                    entries[key].insert('0',value)

                self.row+=1

            else:
                labels[key],entries[key] = self.CreateSettings(value)
                self.row+=len(labels[key])

        return labels,entries

    def FillTheEntries(self,entries,info):
        for key,value in entries.items():
            if type(value)==dict:
                self.FillTheEntries(value,info[key])
            else:
                value.delete("0","end")
                if type(info[key])==str:
                    value.insert("0",info[key])
                else:
                    value.insert("0",os.path.relpath(info[key][0]))

    def ChooseFolder(self,entry):
        folder = filedialog.askdirectory()
        if folder:
            entry.delete("0","end")
            entry.insert("0",os.path.relpath(folder))

    def SaveSettings(self):
        choice = messagebox.askyesno("To Save Press Yes","For saving the settings \nwe need to restart\nPress Yes To Continue")
        if choice:
            self.SaveEntries(self.info,self.entries)
            self.master.UpdateJson(self.info)
            self.master.RestartGUI()

    def SaveEntries(self,info,entries):
        for key,value in info.items():
            if type(value)==dict:
                self.SaveEntries(value,entries[key])
            else:
                if key in self.choose_dir_buttons:
                    info[key] = [os.path.abspath(entries[key].get())]
                else:
                    info[key] = entries[key].get()   

    def Cancel(self):
        self.FillTheEntries(self.entries,self.info)
        self.master.ChangePage(self.master.prev_page)        
