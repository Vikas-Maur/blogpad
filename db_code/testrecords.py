
TEST_RECORD_STRING = "abcdefghijklmnopqrstuvwxyz"
TEST_RECORD_REAL = "tkinter_real"
TEST_RECORD_REAL_CONTENT = r"""
<h1>myCODEnotein HQ</h1>
<div class=\"section\">
<h2>Whats this HQ for?</h2>
<pre><code>All the flight details,flight info ...etc is done here</pre></code>
<h3>We are also having a HQ at YouTube named : myCODEnotein</h2>
<h3>Make sure to visit it as well</h3>
</div>
"""

def CreateTestRecords(bloghandle,start_index):
    blogs = []
    try:
        conn, cursor = bloghandle.connection, bloghandle.cursor
        bloghandle.CreateBlog(TEST_RECORD_REAL)
        cursor.execute(
            f"""INSERT INTO {TEST_RECORD_REAL} VALUES (1,"title","tkinter| by myCODEnotein"),(2,"teleporter","teleporter"),(3,"content","{TEST_RECORD_REAL_CONTENT}")""")
        for i in range(len(TEST_RECORD_STRING) + 1):
            index = start_index + i + 1
            if i == 0:
                name = TEST_RECORD_REAL
            else:
                name = TEST_RECORD_STRING[i - 1] + "(Not Real)"
            blogs.append((name,))
            bloghandle.RegisterBlog(index, name)
        conn.commit()
    except Exception as e:
        print(e)
    return blogs

def DeleteTestRecords(bloghandle):
    try:
        conn, cursor = bloghandle.connection, bloghandle.cursor
        cursor.execute(f"DROP TABLE {TEST_RECORD_REAL}")
        cursor.execute(f"DELETE FROM bloginfo WHERE name='{TEST_RECORD_REAL}'")
        cursor.execute(f"DELETE FROM bloginfo WHERE name LIKE '%(Not Real)'")
        conn.commit()
    except:
        return False
    return True