from tkinter import *
from tkinter import ttk,scrolledtext,filedialog,messagebox,font
from .page import *
from pages.utils import *
import os

class TextPage(Page):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)
        self.content = ""  # A variable for storing the saved content of a blog

        self.defined_tags = (*STYLES.keys(),)

        # Creating all the frames and dividing the page
        self.upside_bar = UpsideBar(self,height=100,bg=COLORS["dark"])
        self.entries = self.upside_bar.entries
        self.upside_bar.pack(side=TOP,fill=X)
        self.upside_bar.grid_propagate(0)

        self.sidebar = SideBar(self,width=350,bg="lightgrey")
        self.sidebar.pack(side=LEFT,fill=Y)
        self.sidebar.grid_propagate(0)
        
        self.text_bar = TextBar(self,bg="grey")
        self.text_bar.pack(side=LEFT,fill=BOTH,expand=True)

        self.shortcuts = {
            "<Control-s>":self.SaveBlog
        }

    def ChangeTag(self,e=None):
        self.text_bar.ChangeTag()

    def InsertLink(self):
        self.text_bar.InsertLink()

    def InsertTabSection(self):
        self.text_bar.InsertTabSection()
    
    def ChooseIMG(self):
        self.text_bar.ChooseIMG()

    def ChooseVideo(self):
        self.text_bar.ChooseVideo()
  
    def InsertTextRecords(self,records,clear_text=False):
        if clear_text:
            self.text_bar.text.delete("1.0","end")
        for record in records:
            self.text_bar.text.insert("insert",record[0],record[1])
            self.text_bar.text.insert("insert","\n\n") 

    def InsertEntries(self,**kwargs):
        entries = self.entries
        for key,value in kwargs.items():
            entries[key].delete("0","end")
            entries[key].insert("0",value)

    def SaveBlog(self,e=None):
        self.text_bar.ConvertToHTML()
        entries = {
            "title":self.entries["title"].get()
            ,"meta_desc":self.entries["meta_desc"].get()
            ,"content":self.text_bar.text.get("1.0","end")
        }
        self.master.SaveBlog(entries)

    def UpdateAllBlogs(self):
        # EVERYTHING IS SAME AS SaveBlog METHOD EXCEPT THAT THIS METHOD USES self.master.SaveFile WHILE THAT METHOD USES self.master.SaveBlog
        self.text_bar.ConvertToHTML()
        entries = {
            "title":self.entries["title"].get()
            ,"meta_desc":self.entries["meta_desc"].get()
            ,"content":self.text_bar.text.get("1.0","end")
        }
        self.master.SaveFile(entries)

class UpsideBar(Frame):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)

        config = {"foreground":"white","background":COLORS["success"],"font":"consolas 18 bold","text":"Save","bd":0,"command":master.SaveBlog}
        self.save_button = HoverableButton(self,on_enter={"background":"darkgreen","foreground":"lightgrey"},**config)
        self.save_button.grid(row=0,column=0,sticky="nsew",rowspan=2,pady=(10,0),padx=20)

        label_config = {"font":"consolas 20 bold","bg":COLORS["dark"],"fg":"white"}

        Label(self,text="Title:",**label_config).grid(row=0,column=1,sticky="nsew",pady=5)
        Label(self,text="Meta Desc:",**label_config).grid(row=1,column=1,sticky="nsew")
        Label(self,text="Language:",**label_config).grid(row=0,column=3,sticky="nsew",padx=(20,0),pady=5)

        self.entries = {
            "title":ttk.Entry(self,font="consolas 16 bold")
            ,"meta_desc":ttk.Entry(self,font="consolas 16 bold")
            ,"language":ttk.Entry(self,font="consolas 16 bold")
        }

        self.entries["title"].grid(row=0,column=2,sticky="nsew",pady=5)
        self.entries["meta_desc"].grid(row=1,column=2,sticky="nsew")
        self.entries["language"].grid(row=0,column=4,sticky="nsew",pady=5)

        shortcut_config = {"background":COLORS["secondary"],"foreground":"white","text":"Show Shortcuts","font":"consolas 20 bold","bd":0}
        
        self.know_shortcuts = HoverableButton(self,on_enter={"background":COLORS["dark"]},**shortcut_config)
        self.know_shortcuts.grid(row=0,column=5,sticky="nsew",rowspan=2,pady=15,padx=20)

class SideBar(Frame):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)
        
        self.tags = master.defined_tags

        label_config = {"font":"consolas 16 bold","bg":"lightgrey"}
        Label(self,text="Tag:",**label_config).grid(row=0,column=0,pady=10,padx=(10,))

        self.tag_box = ttk.Combobox(self,values=self.tags,font="consolas 14 bold")
        self.tag_box.grid(row=0,column=1,pady=10)
        self.tag_box.bind("<<ComboboxSelected>>",master.ChangeTag)

        img_config = {"text":"Insert Img","command":master.ChooseIMG,"font":"consolas 20 bold","foreground":"white","background":"darkblue"}
        self.insert_img = HoverableButton(self,on_enter={"foreground":"darkgrey"},**img_config)
        self.insert_img.grid(row=1,column=0,columnspan=2,padx=10,pady=(10,0),sticky="nsew")

        video_config = {"text":"Insert Video","command":master.ChooseVideo,"font":"consolas 20 bold","foreground":"white","background":COLORS["success"]}
        self.insert_video = HoverableButton(self,on_enter={"foreground":"darkgrey"},**video_config)
        self.insert_video.grid(row=2,column=0,columnspan=2,padx=10,pady=(10,0),sticky="nsew")

        tabsection_config = {"text":"Insert TabSection","command":master.InsertTabSection,"font":"consolas 20 bold","foreground":"white","background":COLORS["secondary"]}
        self.insert_tabsection = HoverableButton(self,on_enter={"foreground":"darkgrey"},**tabsection_config)
        self.insert_tabsection.grid(row=3,column=0,columnspan=2,padx=10,pady=(10,0),sticky="nsew")

        Label(self,text="href:",**label_config).grid(row=4,column=0,padx=10,pady=(10,0))
        self.link_href = ttk.Entry(self,font="consolas 14 bold")
        self.link_href.grid(row=4,column=1,pady=(10,0))

        Label(self,text="LinkText:",**label_config).grid(row=5,column=0,padx=5,pady=(10,0))
        self.link_text = ttk.Entry(self,font="consolas 14 bold")
        self.link_text.grid(row=5,column=1,pady=(10,0))

        link_config = {"text":"Insert The Link","command":master.InsertLink,"font":"consolas 20 bold","foreground":"white","background":COLORS["danger"]}
        self.insert_link = HoverableButton(self,on_enter={"foreground":"darkgrey"},**link_config)
        self.insert_link.grid(row=6,column=0,columnspan=2,padx=10,pady=(10,0),sticky="nsew")

class TextBar(Frame):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)

        self.master = master
        self.grand_master = master.master
        self.tags = master.defined_tags
        self.link_href = self.master.sidebar.link_href
        self.link_text = self.master.sidebar.link_text

        self.tag_box = master.sidebar.tag_box
        self.entries = self.master.upside_bar.entries

        font_property = font.Font(self, font="consolas 18 bold")
        text_config = {"insertbackground":"yellow","bd":0,"font":font_property,"undo":True,"maxundo":-1,"wrap":WORD,"tabs":font_property.measure("    ")}
        self.text = scrolledtext.ScrolledText(self,**text_config)
        self.text.pack(expand=True,fill=BOTH,padx=5,pady=5)
        self.text.bind("<ButtonRelease-1>",self.SetTagBox)
        self.text.bind("<KeyRelease>",self.KeyReleased)

        self.text_shortcuts = {
            # # , "<Control-l>": self.InsertALink
            # , "<Control-t>": self.InsertTabSection
            "<Control-n>": lambda e: self.ShortcutForTag("normal")
            ,"<Control-t>": lambda e: self.ShortcutForTag("notag")
            , "<Control-Key-1>": lambda e: self.ShortcutForTag("h1")
            , "<Control-Key-2>": lambda e: self.ShortcutForTag("h2")
            , "<Control-Key-3>": lambda e: self.ShortcutForTag("h3")
            , "<Control-Key-4>": lambda e: self.ShortcutForTag("code")
            , "<Control-Key-5>": lambda e: self.ShortcutForTag("code+tab")
            , "<Control-Key-6>": lambda e: self.ShortcutForTag("normal")
            , "<Control-Key-7>": lambda e: self.ShortcutForTag("notag")
            ,"<Control-Return>": self.InsertNewLine
            , "<Control-d>": self.CopySectionDown
        }

        self.ConfigTags()
        self.ConfigTextShortcuts()

    def GiveIndexOfSel(self,default=("insert linestart","insert lineend")):
        try:
            i1,i2 = self.text.tag_ranges("sel")
        except:
            i1,i2 = default
        return i1,i2

    def ConfigTextShortcuts(self):
        for key,command in self.text_shortcuts.items():
            self.text.bind(key,command)

    def InsertNewLine(self,e=None):
        self.text.mark_set("insert","insert lineend")
        self.text.insert("insert","\n")
        return "break"

    def CopySectionDown(self,e=None):
        i1,i2 = self.GiveIndexOfSel() # returns index of selected portion or index of insert line: start , end
        text = self.text.get(i1,i2)
        self.text.mark_set("insert",f"{i2}") # makes the index of insert = the last index of : selected portion / current line
        self.InsertNewLine() # inserts a new line
        self.text.insert("insert",text) # inserts text
        self.text.tag_remove("sel",i1,i2)
        return "break"

    def ConfigTags(self):
        config = {"selectbackground":"blue","selectforeground":"white"}
        for tag in self.tags:
            self.text.tag_config(tag,**config,**STYLES[tag])

    def GetLineTag(self,index="insert"):
        line_tag = None
        for tag in self.text.tag_names(f"{index} linestart"):
            if tag in self.tags:
                line_tag = tag
                break
        return line_tag

    def RemoveLineTag(self):
        line_tag = self.GetLineTag()
        if line_tag:
            self.text.tag_remove(line_tag,"insert linestart","insert lineend")

    def ShortcutForTag(self,tag):
        self.tag_box.set(tag)
        self.ChangeTag()

    def ChangeTag(self):
        tag_to_add = self.tag_box.get()
        self.RemoveLineTag()
        if tag_to_add in self.text.tag_names("insert linestart -1l"):
            self.text.tag_add(tag_to_add,"insert linestart -1l","insert lineend")
        else:
            self.text.tag_add(tag_to_add,"insert linestart","insert lineend")
    
    def InsertLink(self):
        href = self.link_href.get()
        text = self.link_text.get()
        if href and text:
            if not self.text.index("insert")==self.text.index("insert linestart"):
                self.InsertNewLine()
            self.text.insert("insert",f"<a href='{href}'>{text}</a>")
            self.link_href.delete("0","end")
            self.link_text.delete("0","end")
        else:
            messagebox.showerror("Cannot Insert The Link","You had left either the href or LinkText box or both empty.\nThat is why we can't insert the link.\nPlease fill the boxes first and then try.")
    
    def InsertTabSection(self):
        if not self.text.index("insert")==self.text.index("insert linestart"):
            self.InsertNewLine()
        self.text.insert("insert","Code,Desc\n#Your Code Here\n---\n#Your Desc Here","code+tab")

    def ChooseFiles(self,title,filetypes,command):
        objects = filedialog.askopenfilenames(title=title,filetypes=filetypes,initialdir=self.grand_master.info["parent_dir"][0])
        if objects:
            if not self.text.index("insert")==self.text.index("insert linestart"):
                self.InsertNewLine()
            for obj in objects:
                command(obj)
   
    def ChooseIMG(self):
        self.ChooseFiles(title="Choose Image / Images(ctrl+click or select at ones for multiple images)",filetypes=(("PNG","*.png"),("JPG","*jpg"),("JPEG","*.jpeg")),command=self.InsertIMG)

    def InsertIMG(self,image):
        rel_path = os.path.relpath(image,self.grand_master.info["parent_dir"][0])
        img = "/"+"/".join(rel_path.split("\\"))
        self.text.insert("insert",f"<img class='img-fluid' alt='' src='{img}'/>")
        self.ShortcutForTag("img")
        self.InsertNewLine()

    def ChooseVideo(self):
        kwargs = {"title":"Choose Video / Videos(ctrl+click or select at ones for multiple videos)","filetypes":(("MP4","*.mp4"),),"command":self.InsertVideo}
        self.ChooseFiles(**kwargs)

    def InsertVideo(self,video):
        rel_path = os.path.relpath(video,self.grand_master.info["parent_dir"][0])
        vid = "/"+"/".join(rel_path.split("\\"))
        self.text.insert("insert",f"<video preload='none' title='If the video does not load then please refresh/reload the page' src='{vid}' controls muted></video>")
        self.ShortcutForTag("video")
        self.InsertNewLine()

    def SetTagBox(self,e=None):
        line_tag = self.GetLineTag()
        if not line_tag:
            line_tag = "normal"

            prev_line_tag = self.GetLineTag("insert -1l")
            if prev_line_tag in ("code","code+tab"):
                line_tag = prev_line_tag

        self.tag_box.set(line_tag)

    def KeyReleased(self,e=None):
        self.SetTagBox()
        self.ChangeTag()
    
    def ConvertToHTML(self):
        tags_to_convert = tuple(TAG_TEMPLATES.keys())
        sno = 0
        section_is_present = False
        for tag in tags_to_convert:
            index = 0
            tag_template = TAG_TEMPLATES[tag]
            func_to_call = eval(tag_template[-1])
            while True:
                try:
                    sno_increment , index_increment = func_to_call(sno, index, tag, tag_template)
                    index += index_increment
                    sno += sno_increment
                except Exception as e:
                    break
            if tag=="h2" and index>0:
                section_is_present = True

        html = self.text.get("1.0","end").strip()
        self.text.delete("1.0","end")
        self.text.insert("1.0",html)

        if section_is_present:
            self.text.insert("end","</div>") # to end the last section


    def ConvertToNormalTag(self,sno,index,tag,tag_template,**kwargs):
        id = f"{tag}-{sno}"
        r = self.text.tag_ranges(tag)[index]

        if index%2==0:
            sno_increment = 1
            index_increment = 2

            if not self.text.get(r,self.text.tag_ranges(tag)[index+1]).strip():
                return sno_increment,index_increment

            text_to_add = tag_template[0].format(id=id,**kwargs)

        else:
            text_to_add = tag_template[1]
            sno_increment = 0
        
        self.text.insert(r,text_to_add,tag)
        index_increment = 1 
        return sno_increment,index_increment

    def ConvertToH2(self,sno,index,tag,tag_template):
        id = f"{tag}-{sno}"
        r = self.text.tag_ranges(tag)[index]
        if index==0:
            sno_increment = 1
            text_to_add = tag_template[0].format(id=id,section_end="")

        elif index%2==0:
            sno_increment = 1
            text_to_add = tag_template[0].format(id=id, section_end="</div>")

        else:
            sno_increment = 0
            text_to_add = tag_template[1]

        self.text.insert(r,text_to_add,tag)
        index_increment = 1
        return sno_increment,index_increment

    def ConvertToCode(self,sno,index,tag,tag_template):
        return self.ConvertToNormalTag(sno,index,tag,tag_template,language=self.entries["language"].get())

    def ConvertToTabSection(self,sno,index,tag,tag_template):
        r1,r2 = self.text.tag_ranges(tag)[index:index+2]
        id = f"{tag}-{sno}"

        text = self.text.get(r1,r2)
        links,blocks = text.split("\n",maxsplit=1)

        blocks = blocks.split("---")
        links = links.split(",")

        html = tag_template[0]["tag"]
        link_html = block_html = ""

        for i,link in enumerate(links):
            kwargs = {
                "active":""
                ,"selected":"false"
                ,"id":f"tab-link-{sno}-{i}"
                ,"target":f"tab-target-{sno}-{i}"
                ,"content":link.strip()
            }
            if i==0:
                kwargs["active"] = "active"
                kwargs["selected"] = "true"
            link_html += tag_template[0]["link"].format(**kwargs)
   
        for i,block in enumerate(blocks):
            kwargs = {
                "active":""
                ,"language":self.entries["language"].get()
                ,"link":f"tab-link-{sno}-{i}"
                ,"id":f"tab-target-{sno}-{i}"
                ,"content":block.strip()
            }
            if i== 0:
                kwargs["active"] = "active"

            block_html += tag_template[0]["tag_block"].format(**kwargs)


        html = html.format(id=id,tag_links=link_html,tag_blocks=block_html)

        self.text.replace(r1,r2,html,"code+tab")

        index_increment = 2
        sno_increment = 1
        return sno_increment,index_increment



if __name__=="__main__":
    root = Tk()
    root.geometry("1300x700+0+0")

    text_page = TextPage(root)
    text_page.pack(fill=BOTH,expand=True)

    root.mainloop()

# from .page import *
# from tkinter import ttk,scrolledtext,filedialog,messagebox,font
# from pages.utils import *
# import os

# class TextPage(Page):
#     def __init__(self,master,**kwargs):
#         super().__init__(master,**kwargs)
#         self.content = ""  # A variable for storing the saved content of a blog

#         # Creating all the frames and dividing the page
#         self.upside_bar = Frame(self,height=100,bg=COLORS["dark"])
#         self.sidebar = Frame(self,width=350,bg="lightgrey")
#         self.text_bar = Frame(self,bg="grey")

#         self.upside_bar.pack(side=TOP,fill=X)
#         self.sidebar.pack(side=LEFT,fill=Y)
#         self.text_bar.pack(side=LEFT,fill=BOTH,expand=True)

#         self.upside_bar.grid_propagate(0)
#         self.sidebar.grid_propagate(0)

#         # UPSIDE_BAR
#         self.save_button = HoverableButton(self.upside_bar
#                                            ,on_enter={"background":"darkgreen","foreground":"lightgrey"}
#                                            ,foreground="white",background=COLORS["success"]
#                                            ,font="consolas 18 bold",text="Save"
#                                            ,bd=0,command=self.SaveBlog)
#         self.save_button.grid(row=0,column=0,sticky="nsew",rowspan=2,pady=(10,0),padx=20)

#         label_config = {
#             "font":"consolas 20 bold"
#             ,"bg":COLORS["dark"]
#             ,"fg":"white"
#         }
#         t_label = Label(self.upside_bar,text="Title:",**label_config)
#         t_label.grid(row=0,column=1,sticky="nsew",pady=5)
#         m_label = Label(self.upside_bar,text="Meta Desc:",**label_config)
#         m_label.grid(row=1,column=1,sticky="nsew")
#         l_label = Label(self.upside_bar,text="Language:",**label_config)
#         l_label.grid(row=0,column=3,sticky="nsew",padx=(20,0),pady=5)

#         self.entries = {
#             "title":ttk.Entry(self.upside_bar,font="consolas 16 bold")
#             ,"meta_desc":ttk.Entry(self.upside_bar,font="consolas 16 bold")
#             ,"language":ttk.Entry(self.upside_bar,font="consolas 16 bold")
#         }

#         self.entries["title"].grid(row=0,column=2,sticky="nsew",pady=5)
#         self.entries["meta_desc"].grid(row=1,column=2,sticky="nsew")
#         self.entries["language"].grid(row=0,column=4,sticky="nsew",pady=5)
#         self.entries["language"].insert(0,"python")

#         self.know_shortcuts = HoverableButton(self.upside_bar,on_enter={"background":COLORS["dark"]}
#                                               ,background=COLORS["secondary"],foreground="white"
#                                               ,text="Show Shortcuts",font="consolas 20 bold"
#                                               ,bd=0)
#         self.know_shortcuts.grid(row=0,column=5,sticky="nsew",rowspan=2,pady=15,padx=20)

#         # SIDEBAR 

#         label_config = {"font":"consolas 16 bold","bg":"lightgrey"}
        
#         self.tags = (*STYLES.keys(),)
#         Label(self.sidebar,text="Tag:",**label_config).grid(row=0,column=0,pady=10,padx=(10,))
#         self.tag_box = ttk.Combobox(self.sidebar,values=self.tags,font="consolas 14 bold")
#         self.tag_box.grid(row=0,column=1,pady=10)
#         self.tag_box.bind("<<ComboboxSelected>>",self.ChangeTag)

#         self.insert_img = HoverableButton(self.sidebar
#                                           ,on_enter={"foreground":"darkgrey"}
#                                           ,foreground="white"
#                                           ,background="darkblue"
#                                           ,font="consolas 20 bold"
#                                           ,text="Insert Img"
#                                           ,command=self.ChooseIMG
#                                           )
#         self.insert_img.grid(row=1,column=0,columnspan=2,padx=10,pady=(10,0),sticky="nsew")

#         self.insert_video = HoverableButton(self.sidebar
#                                           ,on_enter={"foreground":"darkgrey"}
#                                           ,foreground="white"
#                                           ,background=COLORS["success"]
#                                           ,font="consolas 20 bold"
#                                           ,text="Insert Video"
#                                           ,command=self.ChooseVideo
#                                           )
#         self.insert_video.grid(row=2,column=0,columnspan=2,padx=10,pady=(10,0),sticky="nsew")



#         self.insert_tabsection = HoverableButton(self.sidebar
#                                           ,on_enter={"foreground":"darkgrey"}
#                                           ,foreground="white"
#                                           ,background=COLORS["secondary"]
#                                           ,font="consolas 20 bold"
#                                           ,text="Insert TabSection"
#                                           ,command=self.InsertTabSection)
#         self.insert_tabsection.grid(row=3,column=0,columnspan=2,padx=10,pady=(10,0),sticky="nsew")

#         Label(self.sidebar,text="href:",**label_config).grid(row=4,column=0,padx=10,pady=(10,0))
#         self.link_href = ttk.Entry(self.sidebar,font="consolas 14 bold")
#         self.link_href.grid(row=4,column=1,pady=(10,0))

#         Label(self.sidebar,text="LinkText:",**label_config).grid(row=5,column=0,padx=5,pady=(10,0))
#         self.link_text = ttk.Entry(self.sidebar,font="consolas 14 bold")
#         self.link_text.grid(row=5,column=1,pady=(10,0))

#         self.insert_link = HoverableButton(self.sidebar
#                                           ,on_enter={"foreground":"darkgrey"}
#                                           ,foreground="white"
#                                           ,background=COLORS["danger"]
#                                           ,font="consolas 20 bold"
#                                           ,text="Insert The Link"
#                                           ,command=self.InsertLink
#                                           )
#         self.insert_link.grid(row=6,column=0,columnspan=2,padx=10,pady=(10,0),sticky="nsew")

#         # TEXT_AREA
#         font_property = font.Font(self, font="consolas 18 bold")
#         self.text = scrolledtext.ScrolledText(self.text_bar,font="consolas 18 bold"
#                                             ,undo=True,maxundo=-1
#                                             ,wrap=WORD,tabs=font_property.measure("    ")
#                                             ,insertbackground="yellow",bd=0
#                                             )
#         self.text.pack(expand=True,fill=BOTH,padx=5,pady=5)
#         self.text.bind("<ButtonRelease-1>",self.SetTag)
#         self.text.bind("<KeyRelease>",self.KeyReleased)

#         self.text_shortcuts = {
#             "<Control-n>": lambda e: self.AddTagShortcut("normal")
#             # , "<Control-l>": self.InsertALink
#             # , "<Control-t>": self.InsertTabSection
#             , "<Control-Key-1>": lambda e: self.AddTagShortcut("h1")
#             , "<Control-Key-2>": lambda e: self.AddTagShortcut("h2")
#             , "<Control-Key-3>": lambda e: self.AddTagShortcut("h3")
#             , "<Control-Key-4>": lambda e: self.AddTagShortcut("code")
#             , "<Control-Key-5>": lambda e: self.AddTagShortcut("code+tab")
#             , "<Control-Key-6>": lambda e: self.AddTagShortcut("normal")
#             , "<Control-Return>": self.InsertNewLine
#             , "<Control-d>": self.CopySectionDown
#         }

#         self.shortcuts = {
#             "<Control-s>":self.SaveBlog
#         }

#         self.ConfigTag()
#         self.ConfigTextShortcuts()

#     def ChooseFiles(self,title,filetypes,command):
#         objects = filedialog.askopenfilenames(title=title,filetypes=filetypes,initialdir=self.master.info["parent_dir"][0])
#         if objects:
#             for obj in objects:
#                 command(obj)

#     def ChooseIMG(self):
#         self.InsertNewLine()
#         self.ChooseFiles(title="Choose Image / Images(ctrl+click or select at ones for multiple images)"
#                         ,filetypes=(("PNG","*.png"),("JPG","*jpg"),("JPEG","*.jpeg"))
#                         ,command=self.InsertIMG
#         )

#     def InsertIMG(self,image):
#         rel_path = os.path.relpath(image,self.master.info["parent_dir"][0])
#         img = "/"+"/".join(rel_path.split("\\"))
#         self.text.insert("insert linestart",f"<img class='img-fluid' alt='' src='{img}'>","img")
    
#     def ChooseVideo(self):
#         self.InsertNewLine()
#         self.ChooseFiles(title="Choose Video / Videos(ctrl+click or select at ones for multiple videos)"
#                         ,filetypes=(("MP4","*.mp4"),)
#                         ,command=self.InsertVideo
#         )

#     def InsertVideo(self,video):
#         rel_path = os.path.relpath(video,self.master.info["parent_dir"][0])
#         vid = "/"+"/".join(rel_path.split("\\"))
#         self.text.insert("insert linestart",f"<video preload='none' title='If the video does not load then please refresh/reload the page' src='{vid}' controls muted></video>\n","video")

#     def GiveIndexOfSel(self,d1,d2):
#         try:
#             i1,i2 = self.text.index("sel.first"),self.text.index("sel.last")
#         except:
#             i1,i2 = d1,d2
#         return i1,i2

#     def ConfigTag(self):
#         for tag,value in STYLES.items():
#             self.text.tag_config(tag,selectbackground="blue",selectforeground="white",**value)
        
#         config = {
#                 "background":COLORS["success"]
#                 ,"foreground":"white"
#                 ,"selectbackground":"blue"
#                 ,"selectforeground":"white"
#         }
#         self.text.tag_config("img",**config)
#         self.text.tag_config("a",**config)
#         self.text.tag_config("video",**config)

#     def ConfigTextShortcuts(self):
#         for key,command in self.text_shortcuts.items():
#             self.text.bind(key,command)

#     def InsertNewLine(self,e=None):
#         self.text.insert("insert lineend","\n")
#         self.text.mark_set("insert","insert +1l linestart")
#         return "break"

#     def InsertLink(self):
#         href = self.link_href.get()
#         text = self.link_text.get()
#         if href and text:
#             self.InsertNewLine()
#             self.text.insert("insert",f"<a href='{href}'>{text}</a>","a")
#         else:
#             messagebox.showerror("Cannot Insert The Link","You had left either the href or LinkText box or both empty.\nThat is why we can't insert the link.\nPlease fill the boxes first and then try.")

#     def InsertTabSection(self):
#         self.InsertNewLine()
#         self.text.insert("insert","Code,Desc\n#Your Code Here\n---\n#Your Desc Here","code+tab")

#     def CopySectionDown(self,e=None):
#         i1,i2 = self.GiveIndexOfSel("insert","insert")
#         copy = self.text.get(f"{i1} linestart",f"{i2} lineend")
#         self.text.insert(f"{i2} lineend","\n")
#         self.text.mark_set("insert",f"{i2} +1l linestart")
#         self.text.tag_remove("sel",i1,i2)
#         self.text.insert("insert",copy)

#     def AddTagShortcut(self,tag):
#         self.tag_box.set(tag)
#         self.ChangeTag()

#     def GetLineTag(self,index="insert"):
#         line_tag = None
#         for tag in STYLES.keys():
#             if tag in self.text.tag_names(f"{index} linestart"):
#                 line_tag = tag
#                 break
#         return line_tag

#     def RemoveAllTags(self):
#         line_tag = self.GetLineTag()
#         if line_tag:
#             self.text.tag_remove(line_tag,"insert linestart","insert lineend")

#     def ChangeTag(self,e=None):
#         tag = self.tag_box.get()
#         self.RemoveAllTags()
#         if not self.text.get("insert linestart","insert lineend"): # if the line is empty then returns 
#             return
#         if tag in self.text.tag_names("insert linestart -1l"):
#             self.text.tag_add(tag, "insert linestart -1l", "insert lineend")
#         else:
#             self.text.tag_add(tag, "insert linestart", "insert lineend")

#     def SetTag(self,e):
#         tags_in_line = self.text.tag_names("insert linestart")[::-1]
#         tag_setted = False
#         for tag in tags_in_line:
#             if tag in self.tags:
#                 self.tag_box.set(tag)
#                 tag_setted = True
#                 break

#         if not tag_setted:
#             for tag in MULTI_LINER_TAGS:
#                 if tag in self.text.tag_names("insert linestart -1l"):
#                     self.tag_box.set(tag) 
#                     break
#             else:
#                 self.tag_box.set("normal")

#     def CheckIfMultipleTagsExists(self):
#         tags = []
#         also_check = ("img","video")
#         for tag in self.tags:
#             if tag in self.text.tag_names("insert linestart"):
#                 tags.append(tag)
#         if len(tags)>1:
#             self.RemoveAllTags()
#             self.text.tag_add(tags[-1],"insert linestart","insert lineend")
#         else:
#             for tag in also_check:
#                 if tag in self.text.tag_names("insert linestart"):
#                     self.text.tag_remove(tags[0])
#                     break

#     def KeyReleased(self,e):
#         self.SetTag(e)
#         self.ChangeTag(e)
#         self.CheckIfMultipleTagsExists()

#     def InsertTextRecords(self,records,clear_text=False):
#         if clear_text:
#             self.text.delete("1.0","end")
#         for record in records:
#             self.text.insert("insert",record[0],record[1])
#             self.text.insert("insert","\n\n")

#     def InsertEntries(self,**kwargs):
#         entries = self.entries
#         for key,value in kwargs.items():
#             entries[key].delete("0","end")
#             entries[key].insert("0",value)

#     def ConvertToHTMLEntitites(self):
#         entites = {
#             ">":"&gt;"
#             ,"<":"&lt;"
#         }
#         for entity,name in entites.items():
#             while True:
#                 try:
#                     index = self.text.search(entity,"1.0","end")
#                     line_tag = self.GetLineTag(index)
#                     self.text.replace(index,f"{index} +{len(entity)}c",name,line_tag)
#                 except:
#                     break

#     def ConvertToHTML(self):
#         self.ConvertToHTMLEntitites()
#         defined_tags = ("h1","h2","h3","normal","code","code+tab")
#         sno = 0
#         section_is_present = False
#         for tag in defined_tags:
#             index = 0
#             tag_template = TAG_TEMPLATES[tag]
#             while True:
#                 try:
#                     func_to_call = eval(tag_template[-1])
#                     sno_increment , index_increment = func_to_call(sno, index, tag, tag_template)
#                     index += index_increment
#                     sno += sno_increment
#                 except Exception as e:
#                     break
#             if tag=="h2" and index>0:
#                 section_is_present = True

#         if section_is_present:
#             self.text.insert("end","</div>") # to end the last section

#     def ConvertToNormalTag(self,sno,index,tag,tag_template,**kwargs):
#         id = f"{tag}-{sno}"
#         r = self.text.tag_ranges(tag)[index]

#         if index%2==0:
#             sno_increment = 1
#             index_increment = 2

#             if not self.text.get(r,self.text.tag_ranges(tag)[index+1]).strip():
#                 return sno_increment,index_increment

#             text_to_add = tag_template[0].format(id=id,**kwargs)

#         else:
#             text_to_add = tag_template[1]
#             sno_increment = 0
        
#         self.text.insert(r,text_to_add,tag)
#         index_increment = 1 
#         return sno_increment,index_increment

#     def ConvertToH2(self,sno,index,tag,tag_template):
#         id = f"{tag}-{sno}"
#         r = self.text.tag_ranges(tag)[index]
#         if index==0:
#             sno_increment = 1
#             text_to_add = tag_template[0].format(id=id,section_end="")

#         elif index%2==0:
#             sno_increment = 1
#             text_to_add = tag_template[0].format(id=id, section_end="</div>")

#         else:
#             sno_increment = 0
#             text_to_add = tag_template[1]

#         self.text.insert(r,text_to_add,tag)
#         index_increment = 1
#         return sno_increment,index_increment

#     def ConvertToCode(self,sno,index,tag,tag_template):
#         return self.ConvertToNormalTag(sno,index,tag,tag_template,language=self.entries["language"].get())

#     def ConvertToTabSection(self,sno,index,tag,tag_template):
#         r1,r2 = self.text.tag_ranges(tag)[index:index+2]
#         id = f"{tag}-{sno}"

#         text = self.text.get(r1,r2)
#         links,blocks = text.split("\n",maxsplit=1)

#         blocks = blocks.split("---")
#         links = links.split(",")

#         html = tag_template[0]["tag"]
#         link_html = block_html = ""

#         for i,link in enumerate(links):
#             kwargs = {
#                 "active":""
#                 ,"selected":"false"
#                 ,"id":f"tab-link-{sno}-{i}"
#                 ,"target":f"tab-target-{sno}-{i}"
#                 ,"content":link.strip()
#             }
#             if i==0:
#                 kwargs["active"] = "active"
#                 kwargs["selected"] = "true"
#             link_html += tag_template[0]["link"].format(**kwargs)
   
#         for i,block in enumerate(blocks):
#             kwargs = {
#                 "active":""
#                 ,"language":self.entries["language"].get()
#                 ,"link":f"tab-link-{sno}-{i}"
#                 ,"id":f"tab-target-{sno}-{i}"
#                 ,"content":block.strip()
#             }
#             if i== 0:
#                 kwargs["active"] = "active"

#             block_html += tag_template[0]["tag_block"].format(**kwargs)


#         html = html.format(id=id,tag_links=link_html,tag_blocks=block_html)

#         self.text.replace(r1,r2,html,"code+tab")

#         index_increment = 2
#         sno_increment = 1
#         return sno_increment,index_increment

#     def SaveBlog(self,e=None):
#         self.ConvertToHTML()
#         entries = {
#             " title ":self.entries["title"].get()
#             ," meta_desc ":self.entries["meta_desc"].get()
#             ," content ":self.text.get("1.0","end")
#         }
#         self.master.SaveBlog(entries)

#     def UpdateAllBlogs(self):
#         self.ConvertToHTML()
#         entries = {
#             " title ":self.entries["title"].get()
#             ," meta_desc ":self.entries["meta_desc"].get()
#             ," content ":self.text.get("1.0","end")
#         }
#         self.master.SaveFile(entries)