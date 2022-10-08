from socket import *
import encryption
import sqlite3

# create a socket object

s = socket()
try:
    s.setblocking(True)
    s.bind(("localhost", 9000))
    s.listen(5)
    print("Server Running...")

    while True:
        c, a = s.accept()

        # prints address that connection was received from
        print("Received connection from",  a[0])

        message = "Connected to Boss Server. Hello " + a[0]
        bytesvalue = message.encode('utf-8')
        c.send(bytesvalue)

        bid_request = c.recv(2048)

        bid_request = str(encryption.cipher.decrypt(bid_request.decode('utf-8')))
        delim = ','

        bid_request = bid_request.split(delim)
        bidderId = int(bid_request[0])
        itemId = int(bid_request[1])
        bidAmt = int(bid_request[2])

        user_exists = False
        valid_bid = False
        item_exists = False

        try:
            # open Bidder.db
            con = sqlite3.connect('Bidder.db')

            # create cursor for statement execution
            cur = con.cursor()

            # validate bidderId
            cur.execute('select * from Bidder where BidderId = ?', [bidderId])
            row = cur.fetchone()
            if row is not None:  # bidder exists
                user_exists = True
                row = list(row)
            else:
                print("User does not exist.")

            # validate bid amount is less than PrequalifiedUpperLimit

            if row is not None and bidAmt < int(row[3]):
                valid_bid = True
            elif row is None:
                print("Cannot check prequalified upper limit: user does not exist.")
            else:
                print("Bid Amount higher than the allowed prequalified upper limit.")

            # validate itemId
            cur.execute('select * from AuctionItem where ItemId = ?', [itemId])
            row = cur.fetchone()
            if row is not None:  # item exists
                row = list(row)
                item_exists = True
            else:
                print("Item does not exist.")

            # validate bid amount is greater than the item's LowestBidLimit
            if row is not None and bidAmt > int(row[3]):
                valid_bid = True
            elif row is None:
                print("Cannot check lowest bid limit: item does not exist.")
            else:
                print("Bid Amount is lower than the item's lowest bid limit.")

            # validate bid amount is greater than the item's HighestBidderAmount
            if row is not None and bidAmt > int(row[5]):
                valid_bid = True
            elif row is None:
                print("Cannot check highest bidder amount: item does not exist.")
            else:
                print("Bid Amount is lower than the item's highest bidder amount.")

            if user_exists and item_exists and valid_bid:
                cur.execute('''UPDATE AuctionItem
                            SET HighestBidderAmount = ?,
                                HighestBidderId = ?
                            WHERE
                                ItemId = ? ''', (bidAmt, bidderId, itemId))
                cur.execute('select * from AuctionItem')
                con.commit()
                print("Bid Success!")
            else:
                print("Bid Failed!")


        except:
            con.rollback()
            print("Error accessing Bidder.db")

        finally:
            con.close()

except error as e:
    print("Error:",e)
    exit(1)
finally:
    s.close()


