import sqlite3

conn = sqlite3.connect('database.db')
conn.execute("PRAGMA foreign_keys = 1")
print("Opened database successfully")
conn.execute('DROP TABLE IF EXISTS inventory')
conn.execute('DROP TABLE IF EXISTS issued')
conn.execute('DROP TABLE IF EXISTS logindata')
conn.execute('DROP TABLE IF EXISTS issuedto')
conn.execute('DROP TABLE IF EXISTS policestation')
conn.execute('DROP TABLE IF EXISTS battalions')
conn.execute('DROP TABLE IF EXISTS district')



# conn.execute('CREATE TABLE inventory (issuedfrom STRING, productname STRING, date STRING, dateofsurvey STRING, billno STRING, nameoffirm STRING, itemno STRING, quantity STRING, rateperitem STRING, totalamount STRING, crvno STRING)')
# conn.execute('CREATE TABLE issued (issuedfrom STRING, productname STRING, issuedto STRING, district STRING, quantity STRING)')
conn.execute('CREATE TABLE logindata (email STRING, password STRING)')





########### new #########
conn.execute('''CREATE TABLE inventory 
    (
    issuedfrom STRING, 
    productname STRING, 
    date STRING, 
    dateofsurvey STRING, 
    billno STRING, 
    nameoffirm STRING, 
    itemno STRING, 
    quantity STRING, 
    rateperitem STRING, 
    totalamount STRING, 
    crvno STRING UNIQUE)''')


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

conn.execute('''CREATE TABLE issuedTo 
    (issuedfrom STRING, 
    productname STRING ,
    battalion  STRING,
    district  STRING,
    policestation STRING
    quantity STRING)''')



cur = conn.cursor()


cur.execute('INSERT INTO logindata (email, password) VALUES (?,?)', ("jagmohandixit686@gmail.com", "11111111"))
cur.execute('INSERT INTO logindata (email, password) VALUES (?,?)', ("naiktanvi30@gmail.com", "11111111"))



# districts = [('Shimla', ),
#              ('Solan',),
#              ('Police Distt. Baddi',),
#              ('Sirmaur',),
#              ('Kinnaur',),
#              ('Bilaspur',),
#              ('Mandi',),
#              ('Kullu',),
#              ('Lahaul & Spiti',),
#              ('Hamirpur',),
#              ('Chamba',),
#              ('Kangra',),
#              ('Una',),
#              ('Traffic, Tourist and Railway',),
#              ('State CID',),
# ]
#
# battalions = [('HPABN Junga', 1),
#                 ('1st IRBN Bangarh', 13),
#                 ('2nd IRBN Sakoh', 12),
#                 ('3rd IRBN Pandoh', 7),
#                 ('4th IRBN Jangal Beri', 10),
#                 ('5th IRBN Bassi', 6),
#                 ('6th IRBN Kolar', 4),
#               ]
#
# cur.executemany('INSERT INTO district (name) VALUES (?)', districts)
# cur.executemany('INSERT INTO battalions (name, districtId) VALUES (?,?)', battalions)

# cur.execute('INSERT INTO policestation (psname, district) VALUES (?,?)',('P.S. Sadar ',1))
# cur.execute('INSERT INTO vs (psname, district) VALUES (?,?)',('P.S. East', 'Shimla'))



conn.commit()

print(cur.execute("SELECT rowid, * FROM logindata").fetchall())
print("Table created successfully")
conn.close()