from tkinter import *
from . import page
from .utils import MyButton

class InformationPage(page.Page):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)

        self.images = []
        self.current_image = 0

        self.master_shortcuts = {"<Right>":lambda e:self.ChangePage(1),"<Left>":lambda e:self.ChangePage(-1)}

        self.label = Label(self)
        self.label.pack(pady=(50,0))

        self.button_config = {"font":self.font,"bg":"white","bd":0}
        self.prev_button = MyButton(self,text="Previous(key:<--)",command=lambda:self.ChangePage(-1),**self.button_config)
        self.prev_button.ChangeBGOnHover("lightgrey")
        self.prev_button.place(x=150,y=580)

        self.next_button = MyButton(self,text="Next(key:-->)",command=lambda:self.ChangePage(1),**self.button_config)
        self.next_button.ChangeBGOnHover("lightgrey")
        self.next_button.place(x=940,y=580)

    def ChangePage(self,value):
        self.current_image+=value
        if self.current_image==len(self.images):
            self.current_image-=1
            self.CommandAfterLastImage()

        elif self.current_image<0:
            self.current_image=0
        else:
            self.ShowImage()

    def ShowImage(self):
        self.label.config(image=self.images[self.current_image])

    def CommandAfterLastImage(self):
        return

class BlogWritingPage(InformationPage):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)
        self.config(background="grey")

        self.images = (
            PhotoImage(file="images/upsidebar.png")
            ,PhotoImage(file="images/style.png")
            ,PhotoImage(file="images/rule.png")
            ,PhotoImage(file="images/tabsection.png")
            ,PhotoImage(file="images/rules_tabsection.png")
                      )
        self.ShowImage()


class FirstVisit(InformationPage):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)

        self.images = (
            PhotoImage(file="images/firstvisit/0.png")
            ,PhotoImage(file="images/firstvisit/1.png")
            ,PhotoImage(file="images/firstvisit/2.png")
            ,PhotoImage(file="images/firstvisit/3.png")
            ,PhotoImage(file="images/firstvisit/4.png")
            ,PhotoImage(file="images/firstvisit/5.png")
        )
        self.ShowImage()

    def CommandAfterLastImage(self):
        self.master.ChangePage("settingpage")