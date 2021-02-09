from tkinter import *
from tkinter import messagebox
from . import page
from .utils import *

class HomePage(page.Page):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)

        self.config(background="lightgrey")

        self.master_shortcuts = {
            "<Right>":lambda e:self.ChangePage(1)
            ,"<Left>":lambda e:self.ChangePage(-1)
        }

        self.popup_menu=Menu(self)


        self.temp_blogs = master.total_blogs
        self.current_page = 0

        self.search_frame = Frame(self,bg="lightgrey")
        self.search_frame.pack(pady=(50,20))
        self.search_label = Label(self.search_frame
                                  ,bg="lightgrey"
                                  ,font=self.font
                                  ,text="Search:")
        self.search_label.pack(side=LEFT)
        self.search_box = ttk.Entry(self.search_frame,font=self.font)
        self.search_box.pack(side=LEFT)
        self.search_box.bind("<KeyRelease>",func=self.QueryBlogs)
        self.add_new = MyButton(self.search_frame,font=self.font
                              ,text="Add New Blog",bg=COLORS["success"],bd=0
                              ,fg="white",command=self.AddNewBlog)
        self.add_new.pack(side=LEFT,padx=10)
        self.add_new.ChangeBGOnHover(COLORS["primary"])

        self.create_test_record = MyButton(self,font="consolas 13 bold"
                              ,text="Create Test Blogs",bg=COLORS["dark"],bd=0
                              ,fg="white",command=master.CreateTestRecords)
        self.create_test_record.place(x=950,y=2)
        self.delete_test_record = MyButton(self,font="consolas 13 bold"
                              ,text="Delete Test Blogs",bg=COLORS["dark"],bd=0
                              ,fg="white",command=master.DeleteTestRecords)
        self.delete_test_record.place(x=1120,y=2)
        self.create_test_record.ChangeBGOnHover("darkgrey")
        self.delete_test_record.ChangeBGOnHover("darkgrey")


        self.blog_frame = Frame(self,bg="lightgrey")
        self.blog_frame.pack()

        self.blogs = self.CreateBlogButtons()
        self.prev_button = MyButton(self.blog_frame,text="Previous Page(key: <--)",bg=COLORS["secondary"]
                                  ,font=self.font,command=lambda :self.ChangePage(-1))
        self.prev_button.grid(row=4,column=0,sticky="nsew",columnspan=2)
        self.prev_button.ChangeBGOnHover("lightgrey")
        self.next_button = MyButton(self.blog_frame,text="Next Page(key: -->)",bg=COLORS["secondary"]
                                  ,font=self.font,command=lambda :self.ChangePage(1))
        self.next_button.grid(row=4,column=3,sticky="nsew",columnspan=2)
        self.next_button.ChangeBGOnHover("lightgrey")
        self.FillBlogNames()

    def ActivatePage(self):
        super().ActivatePage()
        self.QueryBlogs("")

    def AddNewBlog(self):
        self.master.AddNewBlog()

    def CreateBlogButtons(self):
        blogs = []
        row=column=0
        for i in range(20):
            b=MyButton(self.blog_frame,color="lightgrey",width=15,height=3,bg="white",bd=0,font=self.font
                       ,command=lambda i=i:self.OpenBlog(i))
            b.bind("<Button-3>",func=self.RightClickMenu)
            b.grid(row=row,column=column,sticky="nsew",padx=3,pady=3)
            if column==4:
                row+=1
                column=0
            else:
                column+=1
            blogs.append(b)
        return tuple(blogs)

    def ChangePage(self,page):
        self.current_page+=page
        if self.current_page>len(self.temp_blogs)//len(self.blogs):
            self.current_page-=1
        elif self.current_page<0:
            self.current_page=0
        else:
            self.FillBlogNames()

    def FillBlogNames(self):
        i=self.current_page
        for x in range(20*(i+1)):
            index_of_button = x%len(self.blogs)
            try:
                blogname = self.temp_blogs[x][-1]
            except:
                blogname = ""
            self.blogs[index_of_button].config(text=blogname)

    def QueryBlogs(self,e):
        name = self.search_box.get().strip()
        self.temp_blogs = self.master.QueryBlogs(name)
        self.current_page=0
        self.FillBlogNames()

    def OpenBlog(self,i):
        name = self.blogs[i]["text"]
        if name=="":
            return
        else:
            self.master.OpenBlog(name)

    def RightClickMenu(self,e):
        menu = Menu(self,tearoff=0)
        menu.add_command(label="Delete The Blog",command=lambda:self.DeleteBlog(e.widget))
        menu.tk_popup(e.x_root,e.y_root)

    def DeleteBlog(self,button):
        blog = button["text"]
        if blog!="":
            sure = messagebox.askquestion("Are You Sure?",f"Are you sure you want to delete the blog with blogname\n'{blog}'")
            if sure=="yes":
                self.master.DeleteBlog(blog)
                self.QueryBlogs("")


