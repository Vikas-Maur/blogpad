from tkinter import *
from pages.utils import COLORS

class StartScreen(Tk):
    def __init__(self,main_window):
        super().__init__()

        self.main_window = main_window
        self.overrideredirect(True)

        self.width, self.height = 450, 300
        self.bg = COLORS["dark"]
        self.geometry(f"{self.width}x{self.height}+450+200")
        self.config(bg=self.bg)
        self.attributes("-topmost",True)

        self.label_config = {"bg":self.bg,"fg":"white"}
        self.name_frame = Frame(self)
        self.name_frame.pack(pady=(90,0))

        self.brand_name_list = (
            ("my",{"fg":COLORS["warning"]})
            ,("CODE",{"fg":COLORS["primary"]})
            ,("notein",{"fg":COLORS["danger"]})
        )
        self.name_labels = self.CreateLabels(self.brand_name_list)

        self.insertion_label_x,self.insertion_label_y = 85,90
        self.insertion_cursor = Label(self,width=100
                                      ,anchor="w",font="consolas 30",text=""
                                      ,**self.label_config)
        self.insertion_cursor.place(x=self.insertion_label_x,y=self.insertion_label_y)

        self.brand_tagline = "Your Note Place"
        self.tagline_size = 0
        self.tagline_label = Label(self,font="consolas 13 italic",**self.label_config)
        self.tagline_label.pack()

        self.PlayAnimations()


    def CreateLabels(self,texts):
        labels = []
        for t in texts:
            l = Label(self.name_frame,text=t[0],font="consolas 30 bold",bg=self.bg,**t[1])
            l.pack(side=LEFT)
            labels.append(l)
        return tuple(labels)

    def EndStartScreen(self):
        self.destroy()
        self.main_window.deiconify()

    def PlayAnimations(self):
        self.after(500,self.AnimateBrandName)
        self.after(3000,self.AnimateTagline)
        self.after(4000,self.EndStartScreen)

    def AnimateBrandName(self):
        if self.insertion_label_x>400:
            return
        self.insertion_label_x+=13
        self.insertion_cursor.place(x=self.insertion_label_x,y=self.insertion_label_y)
        self.after(65,self.AnimateBrandName)

    def AnimateTagline(self):
        if self.tagline_size==14:
            return
        self.tagline_size+=1
        self.tagline_label.config(text=self.brand_tagline,font=f"consolas {self.tagline_size} italic")
        self.after(10,self.AnimateTagline)