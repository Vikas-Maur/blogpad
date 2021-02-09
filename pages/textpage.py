from tkinter import *
from tkinter import font,scrolledtext,filedialog,messagebox,simpledialog
from pages import page
from .utils import *

class TextPage(page.Page):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)

        self.first_h2_content = True
        self.show_shortcut_window = None # Variable for window which shows shortcuts

        self.master_shortcuts = {
            "<Control-s>":lambda e:self.SaveBlog()
            ,"<Control-i>":lambda e:self.ChooseIMG()
        }

        self.u_bg = COLORS["dark"]
        self.upside_bar = Frame(self,bg=self.u_bg,height=80)
        self.upside_bar.grid_propagate(False)
        self.upside_bar.pack(side=TOP,fill=X)

        self.save_img = PhotoImage(file="images/save.png")
        self.save_button = MyButton(self.upside_bar,color="darkgreen",command=self.SaveBlog
                                  ,image=self.save_img,text="Save"
                                  ,font="consolas 20 bold",bg=COLORS["success"]
                                  ,compound=LEFT,fg="white")
        self.save_button.grid(row=0,column=0,sticky="nsew",padx=20,pady=10)

        self.t_label = Label(self.upside_bar,text="Title:",bg=self.u_bg,fg="white",font="consolas 20 bold")
        self.t_label.grid(row=0,column=1,sticky="nsew")
        self.title = ttk.Entry(self.upside_bar,font="consolas 20 bold")
        self.title.grid(row=0,column=2)

        self.m_label = Label(self.upside_bar,text="Meta Description:",bg=self.u_bg,fg="white",font="consolas 20 bold")
        self.m_label.grid(row=0,column=3,sticky="nsew",padx=(80,0))
        self.meta_desc = ttk.Entry(self.upside_bar,font="consolas 20 bold")
        self.meta_desc.grid(row=0,column=4)

        self.s_bg = "darkgrey"
        self.sidebar = Frame(self,width=300,bg=self.s_bg)
        self.sidebar.pack(side=LEFT,expand=True,fill=BOTH)

        self.s_label = Label(self.sidebar,text="Style:",bg=self.s_bg,font="consolas 20 bold")
        self.s_label.grid(row=0,column=0,sticky="nsew",pady=10)
        self.style_keys = (*tuple(STYLES.keys()),"img")
        self.style = ttk.Combobox(self.sidebar,font="consolas 13 bold",values=self.style_keys)
        self.style.grid(row=0,column=1,sticky="nsew",pady=10)
        self.style.bind("<<ComboboxSelected>>",self.AddTag)

        self.insert_img = MyButton(self.sidebar,color="darkgreen",command=self.ChooseIMG
                                   ,bg=COLORS["success"],fg="white"
                                   ,text="InsertIMG",font="consolas 18 bold")
        self.insert_img.grid(row=1,column=0,sticky="nsew",pady=(10,0))

        self.insert_tab = MyButton(self.sidebar,color="darkblue",command=self.InsertTabSection
                                   ,bg=COLORS["primary"],fg="white"
                                   ,text="InsertTabSection",font="consolas 18 bold")
        self.insert_tab.grid(row=1,column=1,sticky="nsew",pady=(10,0))

        self.insert_link = MyButton(self.sidebar,color="darkred",command=self.InsertALink
                                   ,bg=COLORS["danger"],fg="white"
                                   ,text="InsertALink",font="consolas 18 bold"
                                    )
        self.insert_link.grid(row=2,column=0,sticky="nsew",pady=10)

        self.shortcut_text = "\n".join(
            ("     -SHORTCUTS-     "
             ,"ctrl+1 For H1"
             ,"ctrl+2 For H2"
             ,"ctrl+3 For H3"
             ,"ctrl+4 For Code"
             ,"ctrl+5 for Code+tab"
             ,"ctrl+i for img"
             ,"ctrl+n for normal"
             ,"ctrl+t for inserting tab"
             ,"ctrl+l for inserting the link"
             ,"ctrl+s for saving"
             )
        )
        self.show_shortcuts = MyButton(self.sidebar
                                       ,color="black",command=self.ShowShortcuts
                                       ,bg=COLORS["dark"],fg="white"
                                       ,text="ShowShortcuts",font="consolas 18 bold"
                                       )
        self.show_shortcuts.grid(row=2,column=1,sticky="nsew",pady=10)

        self.code_tab_rules = MyButton(self.sidebar,color="darkred",command=self.ShowTabSectionRules,justify="left"
                                       ,font="consolas 20 bold",bg=COLORS["danger"],fg="white"
                                       ,text="Click To Know \nThe Rules For Creating\nA Code+Tab Region")
        self.code_tab_rules.grid(row=3,column=0,sticky="nsew",pady=10,columnspan=2)
        self.d_bg="lightgrey"
        self.downside_bar = Frame(self,bg=self.d_bg)
        self.downside_bar.pack(side=TOP,fill=BOTH,expand=True)

        self.font = font.Font(self, font="consolas 20 bold")
        self.text = scrolledtext.ScrolledText(self.downside_bar
                                              ,wrap=WORD,undo=True,maxundo=-1
                                              ,tabs=self.font.measure("    ")
                                              ,insertbackground="gold",font="consolas 20 bold")
        self.text.pack(side=RIGHT,fill=BOTH,expand=True,padx=10,pady=1)
        self.text.bind("<KeyRelease>",self.KeyReleased)
        self.text.bind("<ButtonRelease-1>",self.SetCombobox)

        self.text_shortcuts = {
            "<Control-n>":lambda e: self.AddTagShortcut("normal")
            ,"<Control-l>":self.InsertALink
            ,"<Control-t>":self.InsertTabSection
            ,"<Control-Key-1>":lambda e: self.AddTagShortcut("h1")
            ,"<Control-Key-2>":lambda e: self.AddTagShortcut("h2")
            ,"<Control-Key-3>":lambda e: self.AddTagShortcut("h3")
            ,"<Control-Key-4>":lambda e: self.AddTagShortcut("code")
            ,"<Control-Key-5>":lambda e: self.AddTagShortcut("code+tab")
        }

        self.ConfigStyles()
        self.ConfigTextShortcuts()

    def ShowTabSectionRules(self):
        info_page = self.master.pages["blogwritingpage"]
        self.master.ChangePage("blogwritingpage")
        info_page.current_image = 3
        info_page.ShowImage()

    def ShowShortcuts(self):
        if not self.show_shortcut_window:
            self.show_shortcut_window = Toplevel(self.master,height=600,width=800)
            self.show_shortcut_window.geometry("800x600+300+50")
            l = Label(self.show_shortcut_window
                      ,text=self.shortcut_text
                      ,font="consolas 25 bold"
                      ,justify='left'
                      ,bg="white"
                      ,fg="black")
            l.pack(expand=True,fill=BOTH)
            self.show_shortcut_window.protocol("WM_DELETE_WINDOW",self.OnShortcutWindowClose)
        else:
            self.show_shortcut_window.deiconify()
            self.show_shortcut_window.geometry("800x600+300+50")

    def OnShortcutWindowClose(self):
        self.show_shortcut_window.destroy()
        self.show_shortcut_window = None

    def ConfigTextShortcuts(self):
        for key,func in self.text_shortcuts.items():
            self.text.bind(key,func=func)

    def InsertTitle(self,title):
        self.title.delete(0,"end")
        self.title.insert(0,title)

    def InsertMetaDesc(self,meta_desc):
        self.meta_desc.delete(0,"end")
        self.meta_desc.insert(0,meta_desc)

    def InsertContent(self,records):
        self.text.delete("1.0","end")
        for record in records:
            sno, type, tag, content = record
            self.text.insert("insert",content,("tag",tag))
            self.text.insert("insert","\n\n")

    def ConfigStyles(self):
        for style in self.style_keys:
            if style in STYLES:
                self.text.tag_config(style,selectforeground="white",selectbackground=COLORS["primary"],**STYLES[style])
            else:
                self.text.tag_config(style,selectbackground="blue",selectforeground="white"
                                     ,background=COLORS["success"],foreground="white")

    def InsertNewLine(self,to_ignore_condition=True):
        if (to_ignore_condition or (not self.text.index("insert")==self.text.index("insert linestart"))):
            self.text.insert("insert lineend","\n")
            self.text.mark_set("insert","insert linestart +1l")

    def InsertTabSection(self,e=None):
        self.InsertNewLine(False)
        self.text.insert("insert","Code,Desc\n#Your Code Here\n---\n#Your Desc Here",("tag","code+tab"))
        return "break"

    def InsertALink(self,e=None):
        string = simpledialog.askstring("Enter The Link","Please enter the link and \nthe text to show in place of that link \nseparated by a comma \nas shown in format:\n\n\nformat = link,text_to_show")
        if string:
            string = string.strip()
            list = string.split(",")
            if len(list)==2:
                link,text = list
                self.text.insert("insert",f"<a href='{link}'>{text}</a>")
            else:
                messagebox.showerror("Error While Insertion Of Link","The Format in which you entered the link is wrong.\nPlease write the correct format")
        else:
            messagebox.showerror("Link Not Inserted","You have not inserted the link")
        if e:
            return "break"

    def InsertIMG(self,img):
        self.InsertNewLine(False)
        self.text.insert("insert linestart",f"<img alt='' src='{img}'>",("tag","img"))

    def ChooseIMG(self):
        files = filedialog.askopenfilenames(filetypes=(("PNG","*.png"),("JPG","*jpg"),("JPEG","*.jpeg")))
        if files:
            for i in files:
                self.InsertIMG(i)

    def GiveLineStyle(self,index="insert linestart"):
        style = None
        for tag in self.text.tag_names(index):
            if tag in self.style_keys:
                style=tag
                break
        return style

    def RemoveStyles(self):
        to_remove = self.GiveLineStyle()
        if to_remove:
            self.text.tag_remove(to_remove,"insert linestart","insert lineend")

    def AddTag(self,e=None):
        style = self.style.get()
        self.RemoveStyles()
        i1, i2 = "insert linestart", "insert lineend"

        if style in self.text.tag_names("insert linestart -1l"):
            i1,i2="insert linestart -1l","insert lineend"
        elif style in self.text.tag_names("insert linestart +1l"):
            i1,i2 = "insert linestart", "insert lineend +1l"

        self.text.tag_add(style,i1,i2)
        self.text.tag_add("tag",i1,i2)

    def AddTagShortcut(self,tag):
        self.style.set(tag)
        self.AddTag()

    def MaintainTag(self,e=None):
        style_on_line = self.GiveLineStyle()
        if style_on_line:
            self.style.set(style_on_line)
        else: # written so as to automatically add tag to next line if tag in multi_liner_tag
            self.style.set("normal")
            multi_liner_tags = ("code", "code+tab")
            for tag in multi_liner_tags:
                if tag in self.text.tag_names("insert linestart -1l"):
                    self.style.set(tag)
                    break
        self.AddTag()

    def SetCombobox(self,e=None):
        style = "normal"
        for tag in self.text.tag_names("insert linestart"):
            if tag in self.style_keys:
                style=tag
                break
        self.style.set(style)

    def KeyReleased(self,e=None):
        self.MaintainTag()
        self.SetCombobox()

    def SaveBlog(self):
        title = self.title.get()
        meta_desc = self.meta_desc.get()
        if not (title and meta_desc):
            messagebox.showerror("Error ! Could Not Save","You left the title box or meta_desc box empty")
            return

        records = []
        ranges = self.text.tag_ranges("tag")
        content = "\n<!--Content starts here-->\n"
        for i in range(0,len(ranges),2):
            r1,r2 = ranges[i],ranges[i+1]
            style = self.GiveLineStyle(r1)
            text = self.text.get(r1,r2)
            # text = r"\'".join(text.split("'"))
            # text = r'\"'.join(text.split('"'))
            record = (len(records),"content",style,text)
            content+=self.ConvertToTag(record)
            records.append(record)
        content+="\n</div>\n\n<!--Content ends here-->\n"

        teleporter = self.CreateTeleporter(records)
        records.append((len(records),"title","title",title))
        records.append((len(records),"meta_desc","meta_desc",meta_desc))
        variable_to_pass = (records,title,meta_desc,teleporter,content)
        self.master.SaveBlog(variable_to_pass)

        self.first_h2_content = True

    def ConvertToTag(self,record):
        #(sno,type,tag,content)
        sno, type, tag, content = record
        html = f"\n<!--{tag} STARTS HERE-->\n"
        if tag=="h2" and self.first_h2_content:
            self.first_h2_content = False
            html+="\n<div class='section'>\n"
        elif tag=="h2":
            html+="\n</div>\n<div class='section'>\n"

        if tag=="code+tab":
            html += self.CreateTabSection(sno,content)
        elif tag=="img":
            html += content
        else:
            S_T_G = STYLE_TO_TAG[tag] # STYLE_TO_TAG for a particular tag
            at_start = (
                    S_T_G[0][:S_T_G[-1]]  #initial tag section after which id can be inserted
                    + f" id='{tag}-{sno}'"  #inserting the id with a blank splace at start
                    + S_T_G[0][S_T_G[-1]:] #inserting the rest of tag section needed to insert
                    )
            at_end = S_T_G[1]
            html += at_start+content+at_end

        html+=f"\n<!--{tag} ENDS HERE-->\n"
        return html

    def CreateTabSection(self,sno,content):
        html = f"<div id='tabsection-{sno}'>"
        tab_links,tab_targets = content.split("\n",maxsplit=1)
        html += self.CreateTabLink(sno,tab_links) + self.CreateTabTarget(sno,tab_targets)
        html += "\n</div>"
        return html

    def CreateTabLink(self,unique_no,tab_links):
        html = "\n<nav>\n<div class='nav nav-tabs' role='tablist'>\n"
        links = tab_links.split(",")
        for index,link in enumerate(links):
            a_link = "<a data-bs-toggle='tab' role='tab' class='nav-link "
            if index==0:
                a_link += "active' aria-selected='true' "
            else:
                a_link += "aria-selected='false' "
            a_link += f"id='tabid-{unique_no}-{index}' aria-controls='tabtarget-{unique_no}-{index}' href='#tabtarget-{unique_no}-{index}'>"
            a_link += link+"</a>"
            html += a_link
        html += "\n</div>\n</nav>"
        return html

    def CreateTabTarget(self,unique_no,tab_targets):
        html = "\n<div class='tab-content'>"
        targets = tab_targets.split("---")
        for index,target in enumerate(targets):
            target_tag = f"\n<div role='tabpanel' aria-labelledby='tabid-{unique_no}-{index}' id='tabtarget-{unique_no}-{index}' class='tab-pane fade show "
            if index==0:
                target_tag += "active'><pre>"
            else:
                target_tag += "'><pre>"
            target_tag += f"<code class='python'>{target.strip()}</code></pre></div>"
            html += target_tag
        html += "\n</div>"
        return html

    def CreateTeleporter(self,records):
        teleporter = ""
        h3_found = False
        for record in records:
            sno,type,tag,content=record
            if tag=="h2":
                if h3_found:
                    teleporter += "</nav>"
                    h3_found = False
                teleporter += f"<a class='nav-link' href='#{tag}-{sno}'>{content}</a>"
            elif tag=="h3":
                if not h3_found:
                    teleporter += "<nav class='nav nav-pills flex-column ml-3 my-1'>"
                    h3_found = True
                teleporter += f"<a class='nav-link' href='#{tag}-{sno}'>{content}</a>"
        return teleporter

