"""
Name: Zaria Burton
Date: 10/05/2022
Assignment: Module 6: Encrypt Data in Database
Due Date: 10/05/2022
About this project: This script creates an SQLite3 Bidder db, creates an AuctionItem table,
                    and populates it with 5 lines of data, and displays it
All work below was performed by Zaria Burton
"""

import sqlite3

# create new db
conn = sqlite3.connect('Bidder.db')

# create cursor for statement execution
cur = conn.cursor()

# drop Bidder table from database if exists
try:
    conn.execute('''Drop table AuctionItem;''')
    conn.commit()
    print("AuctionItem table dropped")

except:
    print("AuctionItem table does not exist.")

# create AuctionItem table in db
cur.execute('''create table AuctionItem( 
                ItemId              INTEGER PRIMARY KEY NOT NULL,
                ItemName            TEXT NOT NULL,
                ItemDescription     TEXT NOT NULL,
                LowestBidLimit      INTEGER NOT NULL,
                HighestBidderId     INTEGER NOT NULL DEFAULT 0,
                HighestBidderAmount TEXT NOT NULL DEFAULT 0
                );''')

# save changes
conn.commit()
print('AuctionItem table created.')

data = [(1, 'Oranges',    'orange colored fruit', 5, 0, 0),
        (2, 'Sugar',     'sweet substance', 2, 0, 0),
        (3, 'Almond Flour',  'powdered almonds', 10, 0, 0),
        (4, 'Dutch Processed Cocoa Powder', 'alkalized cocoa powder', 15, 0, 0),
        (5, 'Coffee Powder',  'ground coffee beans', 1, 0, 0)]

# populate table
cur.executemany('insert into AuctionItem values(?,?,?,?,?,?);', data)
conn.commit()
print('Data inserted into AuctionItem table.')

# iterate over rows in table
for row in cur.execute('select * from AuctionItem;'):
    print(row)

conn.close()
print('Connection closed.')

