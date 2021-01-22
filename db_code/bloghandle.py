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
            query = f"""CREATE TABLE {name} (sno INT PRIMARY KEY,type CHAR(20) UNIQUE,content TEXT)"""
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
            query = f"""SELECT * from {self.name} ORDER BY sno"""
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            info = {"title": "", "content": ""}
            for record in records:
                if "title" in record:
                    info["title"] = record[-1]
                else:
                    info["content"] = record[-1]
        except:
            info=None
        return info

    def SaveBog(self,blog):
        if blog["title"]=="":
            return False,"Please Fill The Title Box"
        try:
            title,html,teleporter = blog["title"],blog["content"],blog["teleporter"]
            self.cursor.execute(f"""DELETE FROM {self.name}""")
            self.connection.commit()
            content = html.split('"')
            content = r'\"'.join(content)
            teleporter = r'\"'.join(teleporter.split('"'))
            query = fr"""INSERT INTO {self.name} VALUES (1,"title","{title}") ,(2,"teleporter","{teleporter}") ,(3,"content","{content}")"""
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            return False,e
        return True,"Your Blog Is Saved Successfully"

    def DeleteBlog(self,blog):
        try:
            self.cursor.execute(f'DELETE FROM {self.bloginfo} WHERE name="{blog}"')
            self.cursor.execute(f'DROP TABLE {blog}')
        except:
            return