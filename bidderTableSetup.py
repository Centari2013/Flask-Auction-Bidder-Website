"""
Name: Zaria Burton
Date: 10/05/2022
Assignment: Module 6: Encrypt Data in Database
Due Date: 10/05/2022
About this project: This script creates an SQLite3 Bidder db, creates a Bidder table,
                    and populates it with 6 lines of encrypted data, and displays the encrypted data
All work below was performed by Zaria Burton
"""

import sqlite3
import encryption

# create new db
conn = sqlite3.connect('Bidder.db')

# create cursor for statement execution
cur = conn.cursor()

# drop Bidder table from database if exists
try:
    conn.execute('''Drop table Bidder;''')
    conn.commit()
    print("Bidder table dropped")

except:
    print("Bidder table does not exist.")

# create Bidder table in db
cur.execute('''create table Bidder( 
                BidderId                INTEGER PRIMARY KEY NOT NULL,
                BidderName              TEXT NOT NULL,
                PhoneNumber             TEXT NOT NULL,
                PrequalifiedUpperLimit  INTEGER NOT NULL,
                AppRoleLevel            INTEGER NOT NULL,
                LoginPassword           TEXT NOT NULL
                );''')

# save changes
conn.commit()
print('Bidder table created.')



# populate table

name = str(encryption.cipher.encrypt(b'Chicken Wing').decode('utf-8'))
num = str(encryption.cipher.encrypt(b'111-111-1111').decode('utf-8'))
pwd = str(encryption.cipher.encrypt(b'buffalo').decode('utf-8'))
cur.execute('insert into Bidder values(?,?,?,?,?,?);', (1, name, num, 1000, 1, pwd))
conn.commit()

name = str(encryption.cipher.encrypt(b'Chesse Cake').decode('utf-8'))
num = str(encryption.cipher.encrypt(b'222-222-2222').decode('utf-8'))
pwd = str(encryption.cipher.encrypt(b'fruit').decode('utf-8'))
cur.execute('insert into Bidder values(?,?,?,?,?,?);', (2, name, num, 1000, 2, pwd))
conn.commit()

name = str(encryption.cipher.encrypt(b'Chantilly Cake').decode('utf-8'))
num = str(encryption.cipher.encrypt(b'333-333-3333').decode('utf-8'))
pwd = str(encryption.cipher.encrypt(b'buffalo').decode('utf-8'))
cur.execute('insert into Bidder values(?,?,?,?,?,?);', (3, name, num, 1000, 3, pwd))
conn.commit()

name = str(encryption.cipher.encrypt(b'Taco Pie').decode('utf-8'))
num = str(encryption.cipher.encrypt(b'444-444-4444').decode('utf-8'))
pwd = str(encryption.cipher.encrypt(b'cheese').decode('utf-8'))
cur.execute('insert into Bidder values(?,?,?,?,?,?);', (4, name, num, 3000, 2, pwd))
conn.commit()

name = str(encryption.cipher.encrypt(b'Chocolate Tart').decode('utf-8'))
num = str(encryption.cipher.encrypt(b'555-555-5555').decode('utf-8'))
pwd = str(encryption.cipher.encrypt(b'ganache').decode('utf-8'))
cur.execute('insert into Bidder values(?,?,?,?,?,?);', (5, name, num, 3000, 1, pwd))
conn.commit()

name = str(encryption.cipher.encrypt(b'Stromae Maestro').decode('utf-8'))
num = str(encryption.cipher.encrypt(b'777-777-7777').decode('utf-8'))
pwd = str(encryption.cipher.encrypt(b'papa').decode('utf-8'))
cur.execute('insert into Bidder values(?,?,?,?,?,?);', (7, name, num, 4000, 1, pwd))
conn.commit()

print('Data inserted into Bidder table.')

# iterate over rows in table
for row in cur.execute('select * from Bidder;'):
    print(row)

conn.close()
print('Connection closed.')

