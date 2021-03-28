from tkinter import *
from tkinter import simpledialog,messagebox
from pages import textpage,homepage,settingpage
from other_code import html_to_text,bloghandle,teleporter,menu

import json,os
from string import Template
from bs4 import BeautifulSoup

class BlogPad(Tk):
    def __init__(self):
        super().__init__()

        # Configuring the frames to expand if the root window expands
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)

        # JSON FILE LOCATION
        self.json_file = "other_code/myCODEnotein.json"
        self.info = self.ReadJson()

        # Creating a bloghandle (database stuff)
        self.blog_handle = bloghandle.BlogHandle(self)

        # Creating a menu
        self.menu = menu.BlogPadMenu(self)
        self.config(menu=self.menu)

        # MAIN WINDOW SETTINGS
        # This is not added at the top because after menu is created
        # The window coordinates change (I don't know why)
        # If this is here then the window appears at (0,0) else not due to menu
        self.geometry("1300x700+0+0")
        self.wm_iconbitmap("images/logo.ico")
        self.title("Blogpad by myCODEnotein")

        # Storing the pages
        self.pages = {
            "homepage":homepage.HomePage(self)
            ,"textpage":textpage.TextPage(self)
            ,"settingpage":settingpage.SettingPage(self)
        }
        self.current_page = None
        self.prev_page = None

        # Storing Current Blog
        self.current_blog = None # Changed in : OpenBlog 
                                 # read in : SaveBlog

        # Gridding all the pages
        self.GridAllPages()

        # Showing the first page
        self.OpenPage("homepage")

    def ReadJson(self):
        with open(self.json_file) as f:
            info = json.load(f)
        return info

    def UpdateJson(self,info):
        with open(self.json_file,"w") as f:
            json.dump(info,f)

    def RestartGUI(self):
        self.destroy()
        self.__init__()

    def OpenPage(self,page):
        self.pages[page].tkraise()
        self.pages[page].ActivatePage()
        self.current_page = page

    def ClosePage(self,page):
        self.pages[page].DeActivatePage()
        self.prev_page = page

    def ChangePage(self,page):
        if self.current_page:
            self.ClosePage(self.current_page)
        self.OpenPage(page)

    def GridAllPages(self):
        for page in self.pages.values():
            page.grid(row=0,column=0,sticky="nsew")

    def AddTextToBlog(self,loc):
        with open(loc) as f:
            html = f.read()
        text = html_to_text.HTML_TO_Text(html)
        self.pages["textpage"].InsertTextRecords(text.tag_blocks,True)
        self.pages["textpage"].InsertEntries(**text.entries)

    def OpenBlog(self,record,new_blog=False):
        try:
            name,loc = record
            self.current_blog = record
            self.blog_saved = False
            self.ChangePage("textpage")
            if not new_blog:
                self.AddTextToBlog(loc)
        except Exception as e:
            messagebox.showerror("An Error Occurred",e)  

    def AddBlog(self):
        prompt = "Rules For Giving Name:\n1.NAME CAN CONTAIN ONLY ALPHABETS,DIGITS,AND HYPHENS.\n2.There must not be only digits in the name\n3.THERE MUST NOT BE ANOTHER BLOG WITH SAME NAME\n\nRecommendations:\n1.TRY TO GO FOR SMALLER NAMES\n\nPlease Enter blogname"
        name = simpledialog.askstring("Enter Blog Name", prompt)
        if not name:
            return

        name = name.strip()
        correct_name = self.CheckBlogname(name)
        if correct_name:
            loc = os.path.join(self.info["save_file_in"][0],name+".html")
            try:
                self.blog_handle.RegisterBlog(name, loc)
                self.OpenBlog((name,loc),new_blog=True)
            except Exception as e:
                messagebox.showerror("An Error Occurred",e)
        else:
            messagebox.showerror("Invalid Name", "The name doesn't follow the rules for giving name")

    def CheckBlogname(self,name):
        symbol = "-"
        correct_name = True
        if name.isdigit() or name==symbol:
            correct_name=False
        else:
            for c in name:
                if c.isalnum() or c in symbol:
                    continue
                else:
                    correct_name = False
        return correct_name

    def QueryBlog(self,name):
        return self.blog_handle.QueryBlogs(name)

    def SaveBlog(self,entries):
        try:
            self.config(cursor="watch")
            self.SaveFile(entries)
            self.UpdateIndex()
            self.UpdateSitemap()
            location = self.current_blog[-1]
            messagebox.showinfo("Successfully Saved",f"Successfully Saved The Blog at:\n{location}")
            self.OpenBlog(self.current_blog)
            self.config(cursor="arrow")
        except Exception as e:
            messagebox.showerror("Unable To Save The Blog",e)

    def SaveFile(self,entries):
        with open("template.html") as f:
            template = Template(f.read())
        convertor = teleporter.Teleporter(entries["content"])
        entries["teleporter"] = convertor.teleporter
        location = self.current_blog[-1]
        html = template.safe_substitute(**entries)
        with open(location,"w") as f:
            f.write(html)

    def UpdateAllBlogs(self):
        self.config(cursor="watch")
        error = []
        records = self.blog_handle.QueryBlogs("")
        for record in records:
            self.OpenBlog(record)
            try:
                self.pages["textpage"].UpdateAllBlogs()
            except:
                error.append(record)
        self.config(cursor="arrow")
        self.ChangePage("homepage")
        if len(error)==0:
            messagebox.showinfo("Successfully Saved!","Successfully Saved! all the blogs at their respective locations")
        else:
            messagebox.showinfo("Some blogs are unsaved!",f"We tried to save all the blogs.\nBut few blogs with name,location : {error} \nwere not saved due to some error.")

    def UpdateIndex(self):
        with open("template_index.html") as f:
            template = Template(f.read())
        total_blogs = self.blog_handle.total_blogs
        cards = "<div class='row'><div class='card-group my-4'>"
        index=0
        for name,location in total_blogs:
            url = self.PathToURL(location)
            with open(location) as f:
                html = BeautifulSoup(f.read(),"html.parser")
            meta_desc = html.findChild("meta", {"name": "description"}).get("content").strip()
            card = self.CreateACard(name,meta_desc,url)
            cards += card
            if index%3==2 and index!=len(total_blogs)-1:
                cards+="</div>\n</div>\n\t\t\t\t<div class='row'>\n<div class='card-group my-4'>"

            index+=1

        cards+="</div>\n</div>"
        index_text = template.safe_substitute(cards=cards)
        index_file = os.path.join(self.info["parent_dir"][0],"index.html")
        with open(index_file,"w") as f:
            f.write(index_text)

        return index_file 

    def CreateACard(self,name,meta_desc,url):
        template = """
            <div class="card">
                <div class="card-header fw-bold">$name</div>
                <div class="card-body">
                    <p class="card-text">$meta_desc</p>
                </div>
                <div class="card-footer"><a href="$url" class="btn btn-outline-primary">Read Now</a></div>
            </div>
        """
        template = Template(template)    
        return template.substitute(name=name,meta_desc=meta_desc,url=url)

    def PathToURL(self,path):
        url = os.path.relpath(path,self.info['parent_dir'][0])
        url = "/".join(url.split("\\"))
        url = "/"+url
        return url

    def UpdateSitemap(self):
        urls = self.blog_handle.total_urls
        text = ""
        for name,link in urls:
            text += link + "\n"
        sitemap_file = os.path.join(self.info["parent_dir"][0],"sitemap.txt")
        with open(sitemap_file,"w") as f:
            f.write(text)
        return sitemap_file

if __name__ == "__main__":
    root = BlogPad()
    root.mainloop()