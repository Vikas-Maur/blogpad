from tkinter import Menu,messagebox

class BlogPadMenu(Menu):
    def __init__(self,master, **kwargs):
        super().__init__(master,**kwargs)
        self.master = master

        self.change_page = Menu(self,tearoff=0)
        self.add_cascade(label="ChangePage",menu=self.change_page)

        self.change_page.add_command(label="SettingPage",command=lambda:master.ChangePage("settingpage"))
        self.change_page.add_command(label="HomePage",command=lambda:master.ChangePage("homepage"))

        self.update = Menu(self,tearoff=0)
        self.add_cascade(label="Update",menu=self.update)
        self.update.add_command(label="Update Sitemap",command=self.UpdateSitemap)
        self.update.add_command(label="Update Index",command=self.UpdateIndex)
        self.update.add_command(label="Update All Blogs",command=self.UpdateAllBlogs)

    def UpdateAllBlogs(self):
        continue_ = messagebox.askyesno("Do you want to continue?","This option will update all the blogs present in \nthe blogs table(we have created)\nThe change might be in template or any other code \nand if you want to apply those changes to all the blogs\njust press yes")
        if continue_:
            self.master.UpdateAllBlogs()

    def UpdateIndex(self):
        try:
            already_watch = self.master["cursor"]
            self.master.config(cursor="watch")
            index_file = self.master.UpdateIndex()
            if not already_watch=="watch":
                self.master.config(cursor="arrow")
            messagebox.showinfo("Successfully Updated",f"Successfully updated index.html at\n{index_file}")
        except Exception as e:
            messagebox.showerror("Something went wrong",f"An error occurred while updation of index.html\n\nThe error in as follows:\n\n{e}")
           
    def UpdateSitemap(self):
        try:
            already_watch = self.master["cursor"]
            self.master.config(cursor="watch")
            sitemap_file = self.master.UpdateSitemap()
            if not already_watch=="watch":
                self.master.config(cursor="arrow")
            messagebox.showinfo("Successfully Updated",f"Successfully updated sitemap.txt at\n{sitemap_file}")
        except Exception as e:
            messagebox.showerror("Something went wrong",f"An error occurred while updation of sitemap.txt\n\nThe error in as follows:\n\n{e}")
           
