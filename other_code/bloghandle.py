import mysql.connector as m

class BlogHandle:
    def __init__(self,controller):
        self.controller = controller
        self.info = controller.info

        self.connection,self.cursor = self.CreateConnection()

        self.bloginfo_table = "bloginfo"
        self.sitemap_table = "sitemap"

        self.total_blogs = self.CheckForBlogInfo()# Creates the info table if it does not exists
                                                  # and returns total_blogs

        self.queried_blogs = []

        self.total_urls = self.CheckForSitemap()
        
        self.GiveSnoToBlogs()

    def CreateConnection(self):
        try:
            # CREATES CONNECTION IF THE DATABASE EXISTS
            connection = m.connect(host="localhost",**self.info["database"])
            cursor = connection.cursor()
        except:
            # CREATES DATABASE AND THE CONNECTS TO IT
            database_to_create = self.info["database"]["database"]
            self.info["database"]["database"]=""
            connection = m.connect(host="localhost", **self.info["database"])
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE {database_to_create}")
            cursor.execute(f"USE {database_to_create}")
            self.info["database"]["database"] = database_to_create

        return connection,cursor

    def CheckForBlogInfo(self):
        try:
            self.cursor.execute(f"SELECT name,location FROM {self.bloginfo_table} ORDER BY sno")
            total_blogs = self.cursor.fetchall()
        except:
            self.cursor.execute(f"CREATE TABLE {self.bloginfo_table} (sno INT PRIMARY KEY,name CHAR(50) UNIQUE NOT NULL,location VARCHAR(200) UNIQUE NOT NULL)")
            self.cursor.execute(f"SELECT name,location FROM {self.bloginfo_table} ORDER BY sno")
            total_blogs = self.cursor.fetchall()
        return total_blogs

    def CheckForSitemap(self):
        try:
            self.cursor.execute(f"SELECT * FROM {self.sitemap_table} ORDER BY name")
            total_urls = self.cursor.fetchall()
        except:
            self.cursor.execute(f"CREATE TABLE {self.sitemap_table} (name CHAR(50) PRIMARY KEY,url VARCHAR(200) UNIQUE NOT NULL)")
            self.cursor.execute(f"SELECT * FROM {self.sitemap_table} ORDER BY name")
            total_urls = self.cursor.fetchall()
        return total_urls

    def QueryBlogs(self,name=""):
        self.cursor.execute(f"SELECT name,location FROM {self.bloginfo_table} WHERE name LIKE '{name}%' ORDER BY sno")
        self.queried_blogs = self.cursor.fetchall()
        return self.queried_blogs

    def GiveSnoToBlogs(self):
        # Updates sno of all blogs and makes them consecutive whole numbers starting from zero
        self.total_blogs = self.CheckForBlogInfo()
        self.cursor.execute(f"DELETE FROM {self.bloginfo_table}")
        for index,blog in enumerate(self.total_blogs):
            blog = list(blog)
            blog.insert(0,index)
            blog = tuple(blog)
            self.cursor.execute(f"INSERT INTO {self.bloginfo_table} VALUES {blog}")

        self.connection.commit()

    def RegisterBlog(self,name,location):
        location = r"\\".join(location.split("\\"))
        self.cursor.execute(f"INSERT INTO {self.bloginfo_table} VALUES ({len(self.total_blogs)},'{name}','{location}')")
        self.connection.commit()
        self.total_blogs = self.CheckForBlogInfo()
        self.AddToSitemap(name,location)

    def AddToSitemap(self,name,location):
        url = self.PathToURL(location)
        self.cursor.execute(f"INSERT INTO {self.sitemap_table} VALUES ('{name}','{url}')")
        self.connection.commit()
        self.total_urls = self.CheckForSitemap()

    def PathToURL(self,location):
        url = self.controller.PathToURL(location)
        url = "https://mycodenotein.netlify.app" + url
        return url

    def DeleteBlog(self,name):
        self.cursor.execute(f"DELETE FROM {self.bloginfo_table} WHERE name='{name}'")
        self.connection.commit()
        self.GiveSnoToBlogs()