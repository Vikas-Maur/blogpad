from tkinter import *
from tkinter import font,scrolledtext,filedialog
from pages import page
from .utils import *
from bs4 import BeautifulSoup

class TextPage(page.Page):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)

        self.shortcuts = {
            "<Control-Key-1>": lambda e: self.ShortcutForStyle("h1")
            , "<Control-Key-2>": lambda e: self.ShortcutForStyle("h2")
            , "<Control-Key-3>": lambda e: self.ShortcutForStyle("h3")
            , "<Control-Key-4>": lambda e: self.ShortcutForStyle("code")
            , "<Control-Key-5>": lambda e: self.ShortcutForStyle("code+tab")
        }

        self.id_of_tag = 0

        self.font = font.Font(self, font="consolas 20 bold")
        self.background = "darkblue"

        self.menu_frame = Frame(self,height=100,bg=self.background)
        self.menu_frame.grid_propagate(0)
        self.menu_frame.pack(side=TOP,fill=BOTH,expand=True)

        self.save_img = PhotoImage(file="images/save.png")
        self.save_button = Button(self.menu_frame,text="Save",image=self.save_img,compound=LEFT
                                  ,font=self.font,bg=COLORS["success"],fg="white",command=self.SaveBlog)
        self.save_button.grid(row=0,column=0,sticky="nsew",padx=20,pady=10)

        self.title_entry = MyEntry(self.menu_frame,"Title Of Blog")
        self.title_entry.grid(row=0,column=1,sticky="nsew",padx=(0,20),pady=10)
        self.blogname_entry = MyEntry(self.menu_frame,"Name Of Blog")
        self.blogname_entry.grid(row=0,column=2,sticky="nsew",padx=(0,20),pady=10)
        Label(self.menu_frame,text="Style:",font=self.font,fg="white",bg=self.background).grid(row=0,column=3,sticky="nsew",padx=(0,20),pady=10)
        self.style_combo = ttk.Combobox(self.menu_frame,value=tuple(STYLES.keys()),font=self.font)
        self.style_combo.grid(row=0,column=4,sticky="nsew",padx=(0,20),pady=10)
        self.style_combo.bind("<<ComboboxSelected>>",func=self.AddStyle)

        self.main_frame = PanedWindow(self,orient=HORIZONTAL,height=600,bg="lightgrey")
        self.main_frame.pack(side=TOP,fill=BOTH,expand=True,pady=(10,0),padx=10)

        self.side_frame = Frame(self.main_frame,bg="lightgrey")
        self.main_frame.add(self.side_frame)
        self.takeImg = Button(self.side_frame
                              ,bg=COLORS["danger"],fg="white"
                              ,font=self.font,text="InsertIMG"
                              ,command=self.AskForAndInsertIMG)
        self.takeImg.grid(row=0,column=0,sticky="nsew")
        self.tabsection = Button(self.side_frame
                              ,bg=COLORS["primary"],fg="white"
                              ,font=self.font,text="Know the rules \nof writing a \nblog or tab section"
                              ,command=lambda:self.master.ChangePage("blogwritingpage"))
        self.tabsection.grid(row=1,column=0,sticky="nsew")
        self.shortcut_labels = Label(self.side_frame,bg="lightgrey",font=self.font
                                     ,text="Shortcuts\nctrl+1 for h1\nctrl+2 for h2\nctrl+3 for h3\nctrl+4 for code\nctrl+5 for code+tab")
        self.shortcut_labels.grid(row=2,column=0,sticky="nsew")

        self.text = scrolledtext.ScrolledText(self.main_frame,font="consolas 20 bold"
                                              ,tabs=self.font.measure("    ")
                                              ,insertbackground=COLORS["warning"]
                                              ,undo=True, maxundo=-1
                                              ,wrap=WORD)
        self.main_frame.add(self.text,minsize=950)
        self.text.bind("<KeyRelease>",func=self.KeyReleased)
        self.text.bind("<ButtonRelease-1>",func=self.SetTheStyleInCombo)

        self.ConfigTags()
        self.ConfigShortcuts()

    def InsertUsualTabSection(self):
        if self.text.index("insert")==self.text.index("insert linestart"):
            self.text.insert("insert","Code,Desc\n# Your Code Here\n---\nYour Desc Here","code+tab")

    def InsertTitle(self,title):
        self.InsertInEntry(self.title_entry,title)

    def InsertBlogName(self,name):
        self.InsertInEntry(self.blogname_entry,name)

    def InsertInEntry(self,given_entry,text):
        given_entry.entry.delete("0", "end")
        given_entry.entry.insert("0", text)
        given_entry.place_holder.config(text=given_entry.placeholder + "(filled)")

    def ShortcutForStyle(self,style):
        self.style_combo.set(style)
        self.AddStyle()

    def ConfigShortcuts(self):
        for shortcut,command in self.shortcuts.items():
            self.text.bind(shortcut,func=command)

    def AskForAndInsertIMG(self):
        img = filedialog.askopenfilename(multiple=True,initialdir="C:/Users/vikas/OneDrive/Desktop/myFolder/myCODEnotein/img/")
        if img=="":
            return
        if type(img)==str:
            src = img.split("img/")[-1]
            self.CreateAndInsertIMG(src)
        else:
            for image in img:
                src = image.split("img/")[-1]
                self.CreateAndInsertIMG(src)
                self.text.mark_set("insert","insert lineend")
                self.text.insert("insert lineend","\n")

    def CreateAndInsertIMG(self,src):
        self.text.insert("insert linestart",f'<img src="{src}" alt="">',"img")
        self.text.mark_set("insert","insert -2c")
        self.text.focus_set()

    def ConfigTags(self):
        for style,config in STYLES.items():
            self.text.tag_config(style,selectbackground="blue",**config)
        self.text.tag_config("img",selectbackground="blue",background=COLORS["danger"],foreground="white")

    def RemoveStyles(self,i1,i2):
        rem_style = None
        for style in STYLES.keys():
            if style in (*self.text.tag_names(i1),*self.text.tag_names(i2)):
                self.text.tag_remove(style,i1,i2)
                rem_style=style
                break
        return rem_style

    def AddStyle(self,e=None):
        i1,i2 = "insert linestart","insert lineend"
        if "img" in self.text.tag_names(i1):
            return
        style = self.style_combo.get()
        self.RemoveStyles(i1,i2)
        self.text.tag_add(style,i1,i2)
        if style=="code+tab":
            self.InsertUsualTabSection()

    def SetTheStyleInCombo(self,e=None):
        i = "insert linestart"
        for tag in self.text.tag_names(i):
            if tag in STYLES.keys():
                self.style_combo.set(tag)
                break
        return

    def MaintainStyle(self):
        style = self.style_combo.get()
        i1,i2 = "insert linestart","insert lineend"
        mutli_liner_tags = ("code","code+tab")
        self.RemoveStyles(i1,i2)
        if style in mutli_liner_tags and style in self.text.tag_names("insert -1l linestart"):
            self.text.tag_add(style,"insert -1l linestart",i2)
        elif style in mutli_liner_tags and style in self.text.tag_names("insert +1l linestart"):
            self.text.tag_add(style,i1,"insert +1l linestart")
        else:
            self.text.tag_add(style,i1,i2)

    def KeyReleased(self,e):
        self.SetTheStyleInCombo()
        self.MaintainStyle()

    def ConvertToTabSection(self):
        i=0
        while True:
            tag_ranges = self.text.tag_ranges("code+tab")
            if i==len(tag_ranges):
                break
            if i%2==0:
                r1,r2 = tag_ranges[i],tag_ranges[i+1]
                text = self.text.get(r1,r2)
                tab_and_code = text.split("\n",maxsplit=1)
                list_of_a = tab_and_code[0].split(",")
                list_of_text = tab_and_code[1].split("---")
                tab_section = self.CreateTabSection(i//2,list_of_a,list_of_text)
                self.text.replace(r1,r2,tab_section,"code+tab")
            i+=2

    def CreateTabSection(self,unique_no,list_of_a,list_of_text):
        html = f"""<div id="auto-tabsection-{unique_no}">\n<nav>\n<div class="nav nav-tabs" role="tablist">\n"""
        for index,a in enumerate(list_of_a):
            html+=self.CreateTabLink(unique_no,index,a)
        html+="""\n</div>\n</nav>\n<div class="tab-content">"""
        for index,text in enumerate(list_of_text):
            html+=self.CreateTabTarget(unique_no,index,text)
        html+="\n</div>\n</div>"
        return html

    def CreateTabLink(self,unique_no,index,a):
        a_link = """<a data-bs-toggle="tab" role="tab" class="nav-link """
        if index == 0:
            a_link += 'active" aria-selected="true"'
        else:
            a_link += '" aria-selected="false"'
        a_link += f"""id="auto-tabid-{unique_no}-{index}" aria-controls="auto-tabtarget-{unique_no}-{index}" href="#auto-tabtarget-{unique_no}-{index}">"""
        a_link += a + "</a>"
        return a_link

    def CreateTabTarget(self,unique_no,index,text):
        tab_target = f"""\n<div aria-labelledby="auto-tabid-{unique_no}-{index}"  role="tabpanel" id="auto-tabtarget-{unique_no}-{index}" class="tab-pane fade show """
        if index==0:
            tab_target+='active"><pre>'
        else:
            tab_target+='"><pre>'
        tab_target+=f"<code>{text.strip()}</code></pre></div>\n"
        return tab_target

    def ConvertToStyleHTML(self,style,section_start="",section_end=""):
        # tag:(<tagname>,attributes,textaftertag,beforeendtag)
        tag_info = STYLE_TO_TAG[style]
        tag_start = section_start+f"""<{tag_info[0]} {tag_info[1]} id="{tag_info[0]}-{self.id_of_tag}">{tag_info[2]}"""
        tag_end = f"{tag_info[3]}</{tag_info[0]}>"
        i = 0
        while True:
            tag_ranges = self.text.tag_ranges(style)
            if i==len(tag_ranges):
                break
            if i==0:
                text = tag_start
                self.id_of_tag+=1
            elif i%2==0:
                text = section_end+tag_start
                self.id_of_tag+=1
            elif i==len(tag_ranges)-1:
                text = tag_end
                self.text.insert("end",section_end)
            else:
                text = tag_end
            self.text.insert(tag_ranges[i],text,style)
            i+=1

    def ConvertToHTML(self):
        section_start = "<div class='section'>"
        section_end = "</div>"
        for style in STYLES.keys():
            if style=="h2":
                self.ConvertToStyleHTML(style,section_start,section_end)
            elif style=="code+tab":
                self.ConvertToTabSection()
            else:
                self.ConvertToStyleHTML(style)
        return self.text.get("1.0","end")

    def CreateTeleporter(self,html):
        soup = BeautifulSoup(html,"html.parser")
        teleporter = ""
        elements = soup.find_all("h2")
        for element in elements:
            teleporter+=self.CreateTeleporterLink(element.get("id"),element.text.strip())
            h2 = element.find_next_siblings("h3")
            teleporter+=self.CreateSubLinks(h2)

        return teleporter

    def CreateTeleporterLink(self,id,text):
        link = f"""<a class="nav-link" href="#{id}">{text}</a>"""
        return link

    def CreateSubLinks(self,elements):
        if len(elements)>0:
            html = """<nav class="nav nav-pills flex-column ml-3 my-1" >"""
        else:
            return ""
        for element in elements:
            html+=self.CreateTeleporterLink(element.get("id"),element.text.strip())
        html+="</nav>"
        return html

    def ConvertFromHTML(self,html):
        self.text.delete("1.0","end")
        soup = BeautifulSoup(html,"html.parser")
        h1 = soup.find("h1")
        if h1:
            self.text.insert("insert",h1.text,"h1")
        self.text.insert("insert","\n")
        sections = soup.find_all("div",class_="section")
        for section in sections:
            section_html = section.findChildren(recursive=False)
            for child in section_html:
                name = child.name
                text = child.text.strip()
                if name=="img":
                    self.text.insert("insert",child,name)
                elif name=="div" and "tabsection" in child.get("id"):
                    a_links = child.findChildren("a")
                    tab_targets = child.findChildren("code")
                    links=[]
                    for a in a_links:
                        links.append(a.text.strip())
                    text=",".join(links)+"\n"
                    tab_targets_links=[]
                    for tab in tab_targets:
                        tab_targets_links.append(tab.text.strip())
                    text+="\n---\n".join(tab_targets_links)
                    self.text.insert("insert",text,"code+tab")
                elif name=="pre":
                    self.text.insert("insert", text, "code")
                else:
                    self.text.insert("insert", text, name)
                self.text.insert("insert","\n\n")

    def SaveBlog(self):
        html = self.ConvertToHTML()
        teleporter = self.CreateTeleporter(html)
        title = self.title_entry.entry.get()
        self.ConvertFromHTML(self.text.get("1.0", "end"))
        blog = {
            "title":title,
            "teleporter":teleporter,
            "content":html
        }
        self.master.SaveBlog(blog)
