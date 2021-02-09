try:
    from tkinter import *
    from tkinter import messagebox, simpledialog
    from db_code.bloghandle import BlogHandle
    from db_code import testrecords, renew
    from pages import textpage, homepage, settingspage, informationpage
    import json, re, os
    from startanimation import StartScreen
except ModuleNotFoundError as e:
    module = e.name
    if module in ("mysql",):
        print("You Have Not Installed The GUI.\nOr Some Dependencies Are Missing.\nPlease Follow The Installation_process.txt to know how to install those")
    else:
        print("The Module Named :",module,"is not found.\nWe suspect that you have changed the directory structure\nPlease either follow the directory_strcuture.txt to restore the directory structure or re download the GUI")
    input("Enter Any Key To Exit The Interface")
    exit()

class BlogPad(Tk):
    def __init__(self):
        super().__init__()
        self.iconify()

        self.title("BlogPad - by myCODEnotein")
        self.geometry("1300x700+0+0")
        self.maxsize(width=1300,height=700)
        self.wm_iconbitmap("images/logo.ico")

        self.info_file = "myCODEnotein.json"
        self.info = self.GetInfo()

        self.current_page = ""
        self.prev_page = ""

        if self.info["first_visit"]:
            self.info["first_visit"]=False
            self.UpdateInfo(self.info)
            self.pages={
                "firstvisitpage": informationpage.FirstVisit(self)
                ,"settingpage": settingspage.SettingPage(self, self.info)
            }
            self.GridAllPages()
            self.ChangePage("firstvisitpage")
            return

        self.bloghandle = BlogHandle(self.info["database"])
        self.total_blogs = self.bloghandle.QueryBlogs("")

        self.patterns = {
            "title": re.compile(r"\{\{ title \}\}"),
            "teleporter": re.compile(r"\{\{ teleporter \}\}"),
            "content": re.compile(r"\{\{ content \}\}"),
            "meta_desc": re.compile(r"\{\{ meta_desc \}\}")
        }

        self.pages = {
            "homepage":homepage.HomePage(self)
            ,"textpage":textpage.TextPage(self)
            ,"settingpage":settingspage.SettingPage(self,self.info)
            ,"blogwritingpage":informationpage.BlogWritingPage(self)
            ,"firstvisitpage":informationpage.FirstVisit(self)
        }

        self.menu = BlogpadMenu(self, tearoff=0)
        self.config(menu=self.menu)

        self.GridAllPages()
        self.ChangePage("homepage")

    def GridAllPages(self):
        for page in self.pages.values():
            page.grid(row=0,column=0,sticky="nsew")

    def ChangePage(self,page):
        self.pages[page].tkraise()
        if self.current_page:
            self.pages[self.current_page].DeactivatePage()
        self.pages[page].ActivatePage()

        self.prev_page,self.current_page=self.current_page,page

        try:
            if self.bloghandle.name:
                name = "Selected Blog: " + self.bloghandle.name
            else:
                name = "No Blog Selected"
            self.title(f"BlogPad - by myCODEnotein - {page} | {name}")
        except:
            self.title("BlogPad - by myCODEnotein")

    def QueryBlogs(self,name):
        return self.bloghandle.QueryBlogs(name)

    def GetInfo(self):
        with open(self.info_file) as f:
            info = json.load(f)
        return info

    def UpdateInfo(self,info):
        with open(self.info_file,"w") as f:
            json.dump(info,f)
            self.info = info

    def UpdateDBInfo(self,info):
        self.UpdateInfo(info)
        restart = messagebox.askquestion("Restart","To Apply New Settings You Must Restart The GUI.\nPress Yes To Restart")
        if restart=="yes":
            self.RestartTheGUI()

    def RestartTheGUI(self):
        self.destroy()
        self.__init__()
        self.deiconify()

    def OpenBlog(self,name):
        info = self.bloghandle.OpenBlog(name)
        if info:
            self.ChangePage("textpage")
            page = self.pages["textpage"]
            page.InsertTitle(info["title"])
            page.InsertMetaDesc(info["meta_desc"])
            page.InsertContent(info["content"])

    def AddNewBlog(self):
        prompt = "Rules For Giving Name:\n1.NAME CAN CONTAIN ONLY ALPHABETS,DIGITS,UNDERSCORE AND DOLLOR.\n2.NAME CANT HAVE ONLY DIGITS THAT MEANS \nTHERE MUST BE ATLEAST 1 ALPHABET OR DOLLOR OR UNDERSCORE.\n\nRecommendations:\n1.DON'T USE DOLLAR\n2.TRY TO GO FOR SMALLER NAMES\n3.THERE MUST NOT BE ANOTHER BLOG WITH SAME NAME\n\n(DO YOU KNOW\t: these are exact rules for naming a database/table in sql)\n\nPlease Enter blogname"
        name = simpledialog.askstring("Enter Blog Name",prompt)
        if not name:
            messagebox.showerror("Empty Name Box","You left the name writing box empty.\nIf you want to start a new blog again , \npress the add new blog button and then fill a name in it")
            return

        correct_name = self.CheckBlogname(name)
        if not correct_name:
            messagebox.showerror("Invalid Name","The name doesn't follow the rules for giving name")
            return
        else:
            created = self.bloghandle.CreateBlog(name)
            if created is not True:
                messagebox.showerror("Invalid Name",created)
                return
            self.bloghandle.RegisterBlog(len(self.total_blogs)+1,name)
            self.OpenBlog(name)

    def SaveBlog(self,variables):
        records, title, meta_desc, teleporter, content = variables
        saved = self.bloghandle.SaveBog(records)
        if saved[0]:
            file = self.CreateFile(title, meta_desc, teleporter, content)
            messagebox.showinfo("Successfully Saved!!!",f"Successfully Saved With Name {file}")
        else:
            messagebox.showerror("Error Occurred While Saving",saved[-1])

    def CreateFile(self,title, meta_desc, teleporter, content):
        with open("template.html") as f:
            html = f.read()
        html = self.patterns["title"].sub(title, html, 1)
        html = self.patterns["meta_desc"].sub(meta_desc, html, 1)
        html = self.patterns["teleporter"].sub(teleporter,html,1)
        html = self.patterns["content"].sub(content, html, 1)
        name = self.bloghandle.name
        name = "-".join(name.split("_"))
        dir = self.info["saved_file_dir"]
        if not os.path.isdir(dir):
            dir = os.getcwd()
        file = os.path.join(dir,f"{name}.html")
        with open(file,"w") as f:
            f.write(html)
        return file

    def CheckBlogname(self,name):
        symbols = ("$","_")
        correct_name = True
        if name.isdigit():
            correct_name=False
        else:
            for c in name:
                if c.isalnum() or c in symbols:
                    continue
                else:
                    correct_name = False
        return correct_name

    def CreateTestRecords(self):
        blogs = testrecords.CreateTestRecords(self.bloghandle, len(self.total_blogs))
        if len(blogs)>0:
            self.pages["homepage"].temp_blogs += blogs
            self.pages["homepage"].FillBlogNames()
        else:
            messagebox.showerror("Unable to create blog","Either the blog named tkinter already exists\nor all the test blogs are already created.\nIn second case , delete all the blogs through \nDELETE TEST RECORDS BUTTON\nAnd then again press the \nCREATE TEST RECORDS button")

    def DeleteTestRecords(self):
        deleted_records = testrecords.DeleteTestRecords(self.bloghandle)
        if deleted_records:
            self.pages["homepage"].temp_blogs = self.QueryBlogs("")
            self.pages["homepage"].FillBlogNames()
        messagebox.showinfo("Successfully Deleted","Deleted The Test Records Successfully")

    def GoToPrevPage(self):
        if self.prev_page!="":
            self.ChangePage(self.prev_page)

    def DeleteBlog(self,blog):
        self.bloghandle.DeleteBlog(blog)
        messagebox.showinfo("Successfully deleted blog",f"The blog with name={blog} has successfully been deleted")


class BlogpadMenu(Menu):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)

        self.master = master

        self.change_page_option = Menu(self, tearoff=0)
        self.change_page_option.add_command(label="Go To Homepage", command=lambda: self.ChangePage("homepage"))
        self.change_page_option.add_command(label="Go To -How To Write A Blog?- Page",
                                            command=lambda: self.ChangePage("blogwritingpage"))
        self.change_page_option.add_command(label="Go To -How To Operate?- Page",
                                            command=lambda: self.ChangePage("settingpage"))
        self.change_page_option.add_command(label="Go To Setting Page", command=lambda: self.ChangePage("settingpage"))
        self.add_cascade(label="Change Page", menu=self.change_page_option)

        self.setting_option = Menu(self, tearoff=0)
        self.setting_option.add_command(label="Settings", command=lambda: self.ChangePage("settingpage"))
        self.add_cascade(label="Settings", menu=self.setting_option)

        self.goback_option = Menu(self, tearoff=0)
        self.goback_option.add_command(label="Go Back", command=self.master.GoToPrevPage)
        self.add_cascade(label="Go To Previous Page", menu=self.goback_option)

        self.help_option = Menu(self, tearoff=0)
        self.help_option.add_command(label="How To Write A Blog", command=lambda: self.ChangePage("blogwritingpage"))
        self.help_option.add_command(label="How To Operate?", command=lambda: self.ChangePage("firstvisitpage"))
        self.add_cascade(label="Help", menu=self.help_option)

        self.renew_option = Menu(self,tearoff=0)
        self.renew_option.add_command(label="Renew The GUI (as it was first time)",command=self.Renew)
        self.add_cascade(label="Renew The GUI",menu=self.renew_option)

    def ChangePage(self,page):
        self.master.ChangePage(page)

    def Renew(self):
        sure = messagebox.askquestion("Are You Sure?","Renewing the GUI will remove all the previous data\nincluding all the blogs\nand then will make the GUI as it was first time")
        if sure=="yes":
            renew.Renew(self.master)


if __name__ == '__main__':
    root = BlogPad()
    start_screen = StartScreen(root)
    mainloop()
