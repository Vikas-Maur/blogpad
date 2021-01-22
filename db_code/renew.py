JSON_DATA = {
    "database":{"database":"myCODEnotein","user":"root","password":"123"}
    ,"saved_file_dir":"."
    ,"first_visit":True
}

def Renew(controller):
    cnx,cursor,info = controller.bloghandle.connection,controller.bloghandle.cursor,controller.info
    cursor.execute(f"DROP DATABASE {info['database']['database']}")
    controller.UpdateDBInfo(JSON_DATA)
    cnx.close()

