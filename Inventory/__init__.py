from flask import Flask, redirect, render_template, request, json, flash, url_for, jsonify, session, send_file
import sqlite3 as sql
from Inventory.forms import LoginForm, AdditemForm, SearchForm, RegisterForm
import os, random
from Inventory.data import district, stationdata, battalion

app = Flask(__name__)

app.config['SECRET_KEY'] = "mysecretkey"


@app.route("/", methods=["POST","GET"])
def login():
    if session.get('login') == None:
        form = LoginForm()
        if form.validate_on_submit():
            email = request.form['email']
            password = request.form['password']
            session['productname'] = ""

            try:
                conn = sql.connect('database.db')
                cur = conn.cursor()
                data = cur.execute('SELECT * FROM logindata WHERE email = ?', (email,))
                data = list(data)
            except:
                return render_template('login.html',form = form, error = "Unable to fetch data from database")

            if data and str(data[0][0]) == email and str(data[0][1]) == password:
                session['login'] = True
                session['email'] = email
                return redirect(url_for('mainledger'))
            else:
                return render_template('login.html', form=form, error = "Bad credentials")
        
        return render_template('login.html', form=form)

    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if session.get('login'):
        session.clear()
    return redirect(url_for('login'))

@app.route('/issueing', methods=["POST","GET"])
def issueing():
    if session.get('login'):
        if request.form['type'] == 'assign':
            productId = request.form['product']
            quantity = request.form['quantity']
            session['productId'] = productId
            session['quantity'] = quantity
            session['productname'] = request.form['productname']
            return redirect(url_for('issuedto'))
        else:
            conn = sql.connect("database.db")
            cur = conn.cursor()
            productname = request.form['product']
            data = cur.execute('''SELECT * FROM issued WHERE productname=?''',(productname,)).fetchall()

            return render_template('showAssignDetails.html', data = data)
    
    return redirect(url_for('login'))


@app.route("/issuedto", methods=["POST","GET"])
def issuedto():
    if session.get('login'):
        issuedfrom = request.form.get('issuedfrom')
        district = request.form.get('district')
        battalion_form = request.form.get('battalion')
        station = request.form.get('station')
        qty = request.form.get('quantity')

        if issuedfrom and qty:
            if not session['productId']:
                return render_template('issuedTo.html', count=1, data=stationdata, battalions=battalion,
                                       error="Please select a product from main ledger", successMessage="")
            if int(qty) > int(session['quantity']):
                return render_template('issuedTo.html',count=1,data=stationdata,successMessage="", battalions=battalion, error = "Quantity is greater than remaining products in inventory")


            conn = sql.connect("database.db")
            cur = conn.cursor()
            cur.execute("""INSERT INTO issued (issuedBy, issuedfrom, productname,  district, battalion, quantity, station)
                          VALUES (?,?,?,?,?,?,?)""",(session['email'], issuedfrom, session['productname'],  district,battalion_form, qty, station))

            quantity = int(session['quantity']) - int(qty)
            cur.execute("UPDATE inventory SET quantity=? WHERE uniqueId=?", (quantity, session['productId'],))
            conn.commit()
            conn.close()

            if battalion_form == '1':
                battalion_form = "-"
            elif district == '1':
                district = "-"
                station = "-"
            data = {
            'productname' : session['productname'],
            'issuedBy' : session['email'],
            'district' : district,
            'battalion' : battalion_form,
            'station' : station,
            'qty' : qty,
            }
            session.pop('productId')
            session.pop('quantity')
            return render_template('download-issued.html', **data)

        return render_template('issuedTo.html',count=1,data=stationdata, battalions=battalion, error = "", successMessage="")

    return redirect(url_for('login'))



@app.route('/additem', methods=["POST","GET"])
def additem():
    if session.get('login'):

        form = AdditemForm()
        if form.validate_on_submit():

            addedBy = session['email']
            productname = str(request.form['productname']).lower()
            dateofsurvey = str(request.form['dateofsurvey'])
            billno = str(request.form['billno']).lower()
            nameoffirm = str(request.form['nameoffirm']).lower()
            quantity = str(request.form['quantity'])
            rateperitem = str(request.form['rateperitem'])
            totalamount = str(request.form['totalamount'])


            data = {
                'productname' : productname,
                'dosurvey' : dateofsurvey,
                'billno' : billno,
                'nameoffirm' : nameoffirm,
                'quantity' : quantity,
                'rateperitem' : rateperitem,
                'totalamount' : totalamount
            }

            with sql.connect("database.db") as con:
                cur = con.cursor()
                id = random.randint(100000, 1000000000)

                unique = False

                while not unique:
                    if cur.execute('''SELECT * FROM inventory WHERE uniqueId=?''', (id,)).fetchall():
                        id = random.randint(100000, 1000000000)
                    else:
                        unique = True

                cur.execute("""INSERT INTO inventory (uniqueId, addedBy,  productname, dateofsurvey, billno,
                nameoffirm,  quantity, rateperitem, totalamount) VALUES ( ?, ?, ?,  ?, ?, ?, ?, ?, ?)
                """, (id, addedBy,  productname, dateofsurvey, billno, nameoffirm, quantity, rateperitem, totalamount))
                session['productname'] = productname
            con.commit()
            con.close()
            return render_template('download-item.html', **data)

        return render_template("add-item.html", form=form, successMessage = "")
    return redirect(url_for('login'))


@app.route('/mainledger', methods=["POST","GET"])
def mainledger():
    if session.get('login'):    
        form = SearchForm()
        con = sql.connect("database.db")
        cur = con.cursor()
        data = cur.execute("SELECT * FROM inventory")
        data = list(data)

        if form.validate_on_submit():

            name = str(request.form['search']).lower()
            if name:
                try:
                    data = cur.execute("SELECT * FROM inventory WHERE productname=?",(name,))
                    data = list(data)
                    return render_template("main-ledger.html", form=form, data=data, error="")
                except:
                    return render_template("main-ledger.html", form=form, data=data,
                                           error="Unable to fetch data from database")
        con.commit()
        con.close()
        return render_template("main-ledger.html", form=form, data=data, error = "")

    return redirect(url_for('login'))    



@app.route('/download', methods=["POST","GET"])
def download():
    if request.form['type'] == "excel":
        con = sql.connect("database.db")
        cur = con.cursor()
        data = cur.execute("SELECT * FROM inventory")
        data = list(data)
        return render_template('download-ledger.html', data = data)

@app.route('/register', methods = ['POST','GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS inventory(
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

        cur.execute('''CREATE TABLE IF NOT EXISTS issued(
            issuedBy STRING,
            issuedfrom STRING, 
            productname STRING, 
            district STRING, 
            battalion STRING, 
            station STRING, 
            quantity STRING)'''
                     )

        cur.execute('''CREATE TABLE IF NOT EXISTS logindata(
            email STRING, 
            password STRING)'''
                     )

        cur.execute('INSERT INTO logindata (email,password) VALUES (?,?)', (form.email.data, form.password.data))
        con.commit()
        con.close()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/database_download/<filename>')
def database_download(filename):
    return send_file(filename, as_attachment=True)


@app.route('/district', methods=["POST","GET"])
def district():
    district = request.get_json('name')
    session['district'] = district['name']
    return jsonify(status="success", data=district)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)
 


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


# @app.route('/edit', methods=["POST","GET"])
# def edit():  
    # conn = sql.connect("database.db")
    # conn.execute('CREATE TABLE logindata (email STRING, password STRING)')
    # conn.execute('DROP TABLE IF EXISTS issued')
    # conn.execute('CREATE TABLE issued (issuedfrom STRING, productname STRING, issuedto STRING, district STRING, battalion STRING, station STRING, quantity STRING)')
    # cur = conn.cursor()
    # cur.execute('INSERT INTO logindata (email, password) VALUES (?,?)', ("jagmohandixit686@gmail.com", "11111111"))
    # cur.execute('INSERT INTO logindata (email, password) VALUES (?,?)', ("naiktanvi30@gmail.com", "11111111"))
    # conn.commit()
    # conn.close()
    # return redirect(url_for('home')) 
