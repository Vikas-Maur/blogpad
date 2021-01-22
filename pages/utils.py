from tkinter import Frame,Label,BOTH,Button
from tkinter import ttk

COLORS = {
    "primary":"#0D6EFD",
    "secondary":"#6C757D",
    "success":"#198754",
    "danger":"#DC3545",
    "warning":"#FFC107",
    "info":"#0DCAF0",
    "light":"#F8F9FA",
    "dark":"#212529"
}

STYLES = {
    "normal":{"font":"consolas 18 bold","foreground":"black","background":"white"}
    ,"h1":{"font":"consolas 30 bold","foreground":COLORS["primary"],"background":"white"}
    ,"h2":{"font":"consolas 26 bold","foreground":COLORS["danger"],"background":"white"}
    ,"h3":{"font":"consolas 22 bold","foreground":COLORS["warning"],"background":"white"}
    ,"code":{"font":"consolas 18 bold","foreground":"white","background":"black"}
    ,"code+tab":{"font":"consolas 18 bold","foreground":"white","background":"black"}
}

STYLE_TO_TAG = {
    #tag:(<tagname>,attributes,textaftertag,beforeendtag)
    "normal":("div","class='normal'","","")
    ,"h1":("h1","","","")
    ,"h2":("h2","","""<span class="badge bg-danger"> </span> ""","")
    ,"h3":("h3","","""<span class="badge bg-warning"> </span> ""","")
    ,"code":("pre","","<code>","</code>")
    ,"code+tab":("div","","","")
}

class MyButton(Button):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)

    def ChangeBGOnHover(self,color):
        bg=self.cget("bg")
        self.bind("<Enter>",func=lambda e:self.config(background=color))
        self.bind("<Leave>",func=lambda e:self.config(background=bg))


class MyEntry(Frame):
    def __init__(self,master,placeholder):
        super().__init__(master)

        self.placeholder = placeholder

        self.entry = ttk.Entry(self,font="consolas 20 bold")
        self.entry.pack(expand=True,fill=BOTH)
        self.entry.bind("<FocusIn>",func=self.RemovePlaceHolder)
        self.entry.bind("<FocusOut>",func=self.AddPlaceHolder)

        self.place_holder = Label(self
                                  ,cursor="xterm"
                                  ,text=placeholder+"(empty)",font="consolas 20 bold"
                                  ,fg=COLORS["secondary"],bg="white"
                                  )
        self.place_holder.place(x=1,y=1)
        self.place_holder.bind("<Button-1>",func=self.RemovePlaceHolder)

    def RemovePlaceHolder(self,e):
        self.place_holder.place(x=1,y=-10000)
        self.entry.focus_set()

    def AddPlaceHolder(self,e=None):
        self.place_holder.place(x=1,y=1)
        if len(self.entry.get())>0:
            self.place_holder.config(text=self.placeholder+"(filled)")
        else:
            self.place_holder.config(text=self.placeholder+"(empty)")


