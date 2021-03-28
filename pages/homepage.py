from .page import *
from .utils import COLORS,HoverableButton
from tkinter import ttk
import math

class HomePage(Page):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)

        self.up_frame = Frame(self,height=100,bg="black")
        self.up_frame.pack(side=TOP,fill=X,pady=20,padx=100)
        self.up_frame.pack_propagate(False)

        label = {"font":"consolas 45 bold","bg":"black"}
        l1 = Label(self.up_frame,text="Blogpad - by ",fg="white",**label)
        l1.pack(side=LEFT,padx=(120,0))
        l2 = Label(self.up_frame,fg=COLORS["warning"],text="my",**label)
        l2.pack(side=LEFT)
        l3 = Label(self.up_frame,fg=COLORS["primary"],text="CODE",**label)
        l3.pack(side=LEFT)
        l4 = Label(self.up_frame,fg=COLORS["danger"],text="notein",**label)
        l4.pack(side=LEFT)

        self.down_frame = Frame(self)
        self.down_frame.pack(side=TOP,fill=BOTH,expand=True,pady=20,padx=100)

        self.search_frame = Frame(self.down_frame,bg="darkgrey",width=300)
        self.search_frame.pack(side=LEFT,fill=Y)
        search_label = Label(self.search_frame,bg="darkgrey",text="Search For Blogs",font="consolas 20 bold")
        search_label.pack(side=TOP,pady=(20,10))

        self.search_box = ttk.Entry(self.search_frame,font="consolas 16 bold")
        self.search_box.bind("<KeyRelease>",func=self.QueryBlog)
        self.search_box.pack(side=TOP,pady=(0,20))

        self.add_new = HoverableButton(self.search_frame,fg="white"
                                       ,on_enter={"background":COLORS["success"]},bg=COLORS["danger"]
                                       ,text="Add New Blog\n(ctrl+a)",font="consolas 18 bold"
                                       ,command=self.AddBlog)
        self.add_new.pack(side=TOP,fill=BOTH,pady=20)

        self.blog_frame = Frame(self.down_frame,bg="lightgrey")
        self.blog_frame.pack(expand=True,fill=BOTH)

        self.blog_buttons = self.CreateBlogButtons()

        self.prev = HoverableButton(self.blog_frame
                                    ,on_enter={"background":COLORS["warning"]}
                                    ,font="consolas 18 bold",foreground="white"
                                    ,background=COLORS["danger"],text="Prev Page"
                                    ,command=lambda:self.ChangePage(-1))
        self.prev.grid(row=4,column=0,sticky="nsew",columnspan=2,padx=10)

        self.next = HoverableButton(self.blog_frame
                                    ,on_enter={"background":COLORS["warning"]}
                                    ,font="consolas 18 bold",foreground="white"
                                    ,background=COLORS["danger"],text="Next Page"
                                    ,command=lambda:self.ChangePage(1))
        self.next.grid(row=4,column=3,sticky="nsew",columnspan=2,padx=10)

        self.queried_blogs = self.master.blog_handle.total_blogs
        self.blogs_showed = {}
        self.page_no = 0

        self.FillBlogNames()

        self.shortcuts = {"<Control-a>":self.AddBlog}

    def AddBlog(self,e=None):
        self.master.AddBlog()
        return "break"

    def CreateBlogButtons(self):
        row=col=0
        config = {"bd":0,"font":"consolas 16 bold","wrap":125,"background":"darkgrey","width":12,"height":3}
        buttons = []
        for i in range(20):
            button = HoverableButton(self.blog_frame,on_enter={"background":"lightgrey"}
                                     ,command=lambda button_no=i:self.OpenBlog(button_no),**config)
            button.grid(row=row,column=col,padx=10,pady=10,sticky="nsew")
            if col==4:
                col=0
                row+=1
            else:
                col+=1
            buttons.append(button)
        return tuple(buttons)

    def FillBlogNames(self):
        no_of_buttons = len(self.blog_buttons)
        r1,r2 = self.page_no*no_of_buttons , (self.page_no+1)*no_of_buttons
        for i in range(r1,r2):
            button_no = i%no_of_buttons
            try:
                record = self.queried_blogs[i]
            except:
                record = ('','')
            self.blog_buttons[button_no].config(text=record[0])
            self.blogs_showed[button_no] = record

    def ChangePage(self,change):
        self.page_no += change
        max_page_no = math.ceil(len(self.queried_blogs)/len(self.blog_buttons))-1
        if self.page_no>max_page_no:
            self.page_no -= change
        elif self.page_no<0:
            self.page_no = 0
        else:
            self.FillBlogNames()

    def OpenBlog(self,button_no):
        record = self.blogs_showed[button_no]
        if record[0]=='':
            return
        self.master.OpenBlog(record)


    def QueryBlog(self,e):
        self.queried_blogs = self.master.QueryBlog(self.search_box.get())
        self.FillBlogNames()





