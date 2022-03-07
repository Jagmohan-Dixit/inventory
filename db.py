import sqlite3

conn = sqlite3.connect('database.db')
conn.execute("PRAGMA foreign_keys = 1")
print("Opened database successfully")
conn.execute('DROP TABLE IF EXISTS inventory')
conn.execute('DROP TABLE IF EXISTS issued')
conn.execute('DROP TABLE IF EXISTS issuedTo')
conn.execute('DROP TABLE IF EXISTS logindata')
conn.execute('DROP TABLE IF EXISTS policestation')
conn.execute('DROP TABLE IF EXISTS battalions')
conn.execute('DROP TABLE IF EXISTS district')


conn.execute('''CREATE TABLE inventory(
    uniqueId INTEGER,
    addedBy STRING, 
    productname STRING, 
    dateofsurvey STRING, 
    billno STRING, 
    nameoffirm STRING, 
    quantity STRING, 
    rateperitem STRING, 
    totalamount STRING)'''
)

conn.execute('''CREATE TABLE issued(
    issuedBy STRING,
    issuedfrom STRING, 
    productname STRING, 
    district STRING, 
    battalion STRING, 
    station STRING, 
    quantity STRING)'''
)

conn.execute('''CREATE TABLE logindata(
    email STRING, 
    password STRING)'''
)


########### new #########
# conn.execute('''CREATE TABLE inventory
#     (
#     issuedfrom STRING,
#     productname STRING,
#     date STRING,
#     dateofsurvey STRING,
#     billno STRING,
#     nameoffirm STRING,
#     itemno STRING,
#     quantity STRING,
#     rateperitem STRING,
#     totalamount STRING,
#     crvno STRING UNIQUE)''')
#
# conn.execute('''CREATE TABLE issued
#     (issuedfrom STRING,
#     productname STRING ,
#     battalion  STRING,
#     district  STRING,
#     policestation STRING
#     quantity STRING)''')
#
#
# cur = conn.cursor()
#
#
# cur.execute('INSERT INTO logindata (email, password) VALUES (?,?)', ("jagmohandixit686@gmail.com", "11111111"))
# cur.execute('INSERT INTO logindata (email, password) VALUES (?,?)', ("naiktanvi30@gmail.com", "11111111"))
#
# conn.commit()
#
# print(cur.execute("SELECT rowid, * FROM logindata").fetchall())
# print("Table created successfully")
# conn.close()


# conn.execute('''CREATE TABLE district (
#     districtId INTEGER PRIMARY KEY AUTOINCREMENT,
#     name STRING)''')
#
# conn.execute('''CREATE TABLE battalions (
#     battalionId INTEGER PRIMARY KEY AUTOINCREMENT,
#     name STRING,
#     districtId INTEGER references district(districtId))''')
#
# conn.execute('''CREATE TABLE policestation (
#     psId INTEGER PRIMARY KEY AUTOINCREMENT,
#     psname STRING,
#     districtId INTEGER references district(districtId))''')

# cur.executemany('INSERT INTO district (name) VALUES (?)', districts)
# cur.executemany('INSERT INTO battalions (name, districtId) VALUES (?,?)', battalions)

# cur.execute('INSERT INTO policestation (psname, district) VALUES (?,?)',('P.S. Sadar ',1))
# cur.execute('INSERT INTO vs (psname, district) VALUES (?,?)',('P.S. East', 'Shimla'))

