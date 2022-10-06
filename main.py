"""
Name: Zaria Burton
Date: 10/05/2022
Assignment: Module 6: Encrypt Data in Database
Due Date: 10/05/2022
About this project: This script creates a flask website that accesses encrypted data in the Bidder.db
                    and encrypts and decrypts data as necessary for security
All work below was performed by Zaria Burton
"""

from flask import Flask, render_template, request, session, flash
import sqlite3
import os
import encryption

app = Flask(__name__)


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html', name=session['name'])


@app.route('/enternewbidder')
def new_bidder():
    if not session.get('logged_in'):
        return render_template('login.html')
    elif session.get('level_1'):
        return render_template('bidder.html')
    else:
        flash('Page not found.')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if not session.get('logged_in'):
        return render_template('login.html')
    elif session.get('level_1'):
        if request.method == 'POST':
            msg = []
            try:
                nm = request.form['Name']
                pn = request.form['Phone Number']
                pul = request.form['Prequalified Upper Limit']
                arl = request.form['App Role Level']
                pwd = request.form['Login Password']

                # validate input
                error = False
                try:
                    pul = int(pul)
                    arl = int(arl)
                except ValueError:
                    msg.append("Prequalified upper limit and app role level must be numerical integers.")
                    error = True
                    pass

                if not nm or nm.isspace():
                    msg.append("Name field cannot be empty.")
                if not pn or pn.isspace():
                    msg.append("Phone number field cannot be empty.")
                if not pul or pul < 0:
                    msg.append("Prequalified upper limit field cannot be empty.")
                if not arl or not (1 <= arl <= 3):
                    msg.append("App role level must be an interger from 1 to 3.")
                if not pwd or pwd.isspace():
                    msg.append("Login password field cannot be empty.")

                if error:
                    raise ValueError("Input Error")

                nm = str(encryption.cipher.encrypt(bytes(nm, 'utf-8')).decode('utf-8'))
                pn = str(encryption.cipher.encrypt(bytes(pn, 'utf-8')).decode('utf-8'))
                pwd = str(encryption.cipher.encrypt(bytes(pwd, 'utf-8')).decode('utf-8'))

                with sqlite3.connect("Bidder.db") as con:
                    cur = con.cursor()

                    cur.execute(
                        "INSERT INTO Bidder (BidderName,PhoneNumber,PrequalifiedUpperLimit,AppRoleLevel,LoginPassword) VALUES (?,?,?,?,?);",
                        (nm, pn, pul, arl, pwd))

                    con.commit()
                    msg.append("Record successfully added.")

            except not ValueError:
                msg.clear()
                msg.append("Error adding record.")

            finally:
                return render_template("result.html", msgs=msg)
                con.close()
    else:
        flash('Page not found.')


@app.route('/list_bidders')
def list_bidders():
    if not session.get('logged_in'):
        return render_template('login.html')
    elif session.get('level_1') or session.get('level_2'):
        con = sqlite3.connect("Bidder.db")
        con.row_factory = sqlite3.Row

        cur = con.cursor()
        cur.execute("select * from Bidder")

        rows = cur.fetchall()
        rows = [dict(row) for row in rows]
        for row in rows:
            row["BidderName"] = str(encryption.cipher.decrypt(bytes(row["BidderName"], 'utf-8')).encode('utf-8').decode('utf-8'))
            row["PhoneNumber"] = str(encryption.cipher.decrypt(bytes(row["PhoneNumber"], 'utf-8')).encode('utf-8').decode('utf-8'))

        print(rows)

        return render_template("list_bidders.html", rows=rows)
    else:
        flash('Page not found.')


@app.route('/login', methods=['POST'])
def do_login():
    try:
        nm = request.form['username']
        nm = str(encryption.cipher.encrypt(bytes(nm, 'utf-8')).decode('utf-8'))

        pwd = request.form['password']
        pwd = str(encryption.cipher.encrypt(bytes(pwd, 'utf-8')).decode('utf-8'))

        with sqlite3.connect("Bidder.db") as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()

            sql_select_query = """select * from Bidder where BidderName = ? and LoginPassword = ?"""
            cur.execute(sql_select_query, (nm, pwd))

            row = cur.fetchone()
            if (row != None):
                session['logged_in'] = True
                session['name'] = str(encryption.cipher.decrypt(bytes(nm, 'utf-8')).encode('utf-8').decode('utf-8'))

                if int(row['AppRoleLevel']) == 1:
                    session['level_1'] = True
                elif int(row['AppRoleLevel']) == 2:
                    session['level_2'] = True
                elif int(row['AppRoleLevel']) == 3:
                    session['level_3'] = True

            else:
                session['logged_in'] = False
                flash('invalid username and/or password!')
    except:
        con.rollback()
        flash("error in insert operation")
    finally:
        con.close()
    return home()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    session['level_1'] = False
    session['level_2'] = False
    session['level_3'] = False
    session['name'] = ""
    return home()


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
