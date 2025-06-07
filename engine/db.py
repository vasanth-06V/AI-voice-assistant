import sqlite3

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

#create a new table in data base if not exist
query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)

#add a data block into existing table table
# query = "INSERT INTO sys_command VALUES (null,'Google Chrome','C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')"
# cursor.execute(query)
# con.commit()

#delete a table created
#cursor.execute("DROP TABLE IF EXISTS table_name")

query ="CREATE TABLE IF NOT EXISTS web_commands(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)

# query = "INSERT INTO web_commands VALUES (null,'youtube','https://www.youtube.com/')"
# cursor.execute(query)
# con.commit()

# query = "INSERT INTO contacts VALUES (null,'kittu','123456789','')"
# cursor.execute(query)
# con.commit()