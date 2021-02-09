import mysql.connector as m

class BlogHandle:
    def __init__(self,info):
        self.bloginfo = "bloginfo"
        try:
            self.connection = m.connect(host="localhost", **info)
            self.cursor = self.connection.cursor()
        except:
            self.connection = m.connect(host="localhost",user=info["user"],password=info["password"]
                                        ,database="")
            self.cursor = self.connection.cursor()
            self.cursor.execute(f"CREATE DATABASE {info['database']}")
            self.cursor.execute(f"USE {info['database']}")
            self.CreateBlogInfoTable()
            self.connection.close()
            self.__init__(info)

        self.name = None
        self.CreateBlogInfoTable()
        self.InitialiseBlogs()

    def CreateBlogInfoTable(self):
        try:
            query = f"""CREATE TABLE {self.bloginfo} (sno INT PRIMARY KEY,name CHAR(40) UNIQUE KEY) """
            self.cursor.execute(query)
        except:
            return

    def InitialiseBlogs(self):
        blogs = self.QueryBlogs("")
        self.cursor.execute(f"DELETE FROM {self.bloginfo}")
        for index,blog in enumerate(blogs):
            self.cursor.execute(f"""INSERT INTO bloginfo VALUES({index},"{blog[0]}")""")
        self.connection.commit()

    def QueryBlogs(self,name):
        query = f"""SELECT name FROM {self.bloginfo} WHERE name LIKE "{name}%" ORDER BY sno """
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        return records

    def CreateBlog(self,name):
        try:
            query = f"""CREATE TABLE {name} (sno INT PRIMARY KEY,type CHAR(20),tag CHAR(20),content TEXT)"""
            # query = f"""CREATE TABLE {name} (sno INT PRIMARY KEY,type CHAR(20) UNIQUE,content TEXT)"""
            self.cursor.execute(query)
            return True
        except Exception as e:
            return e

    def RegisterBlog(self,sno,name):
        try:
            query = f"""INSERT INTO {self.bloginfo} VALUES ({sno},"{name}")"""
            self.cursor.execute(query)
            self.connection.commit()
            return True
        except Exception as e:
            return e

    def OpenBlog(self,name):
        try:
            self.name = name

            self.cursor.execute(f"SELECT content FROM {name} WHERE type='title'")
            title = self.cursor.fetchall()[0][0]

            self.cursor.execute(f"SELECT content FROM {name} WHERE type='meta_desc'")
            meta_desc = self.cursor.fetchall()[0][0]

            self.cursor.execute(f"SELECT * FROM {name} WHERE type='content'")
            content = self.cursor.fetchall()

            info = {"title":title,"meta_desc":meta_desc,"content":content}
        except Exception as e:
            info = {"title":"","meta_desc":"","content":""}
        return info

    def SaveBog(self,records):
        try:
            self.cursor.execute(f"DELETE FROM {self.name}")
            for record in records:
                self.cursor.execute(f"INSERT INTO {self.name} VALUES {record}")
            self.connection.commit()
        except Exception as e:
            return False,e
        return (True,)

    def DeleteBlog(self,blog):
        try:
            self.cursor.execute(f'DELETE FROM {self.bloginfo} WHERE name="{blog}"')
            self.cursor.execute(f'DROP TABLE {blog}')
        except:
            return