import mariadb
def connectToDatabase():
    """make a connection to the database. On success, returns the cursor"""
    try:
        conn = mariadb.connect(user="mato",password="start123",
        host="localhost",port=3306,database="overview")
        return conn.cursor()
    except mariadb.Error as e:
        return 0