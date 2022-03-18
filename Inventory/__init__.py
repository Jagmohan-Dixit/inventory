import sys

from flask import Flask, redirect, render_template, request, json, url_for, jsonify, session, send_file
import sqlite3 as sql
from Inventory.forms import LoginForm, AdditemForm, SearchForm, RegisterForm, UpdateItemForm
import os, random
from Inventory.data import district, stationdata, battalion

app = Flask(__name__)

app.config['SECRET_KEY'] = "mysecretkey"


@app.route("/", methods=["POST","GET"])
def login():
    # if session.get('login') == None:
        form = LoginForm()
        if form.validate_on_submit():
            email = request.form['email'].lower()
            password = request.form['password'].lower()
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
    # return redirect(url_for('mainledger'))

@app.route('/logout')
def logout():
    if session.get('login'):
        session.clear()
    return redirect(url_for('login'))

@app.route('/retrieving', methods=["POST","GET"])
def retrieving():
    if session.get('login'):
        retrievedTo = str(request.form.get('retrievedTo')).lower()
        district = str(request.form.get('district')).lower()
        battalion_form = str(request.form.get('battalion')).lower()
        station = str(request.form.get('station')).lower()
        substation = str(request.form.get('substation')).lower()
        qty = request.form.get('quantity')

        if retrievedTo and qty:

            if session['productId'] == None:
                return render_template('retrieve.html', count=1, data=stationdata, battalions=battalion,
                                       error="Please select a product from main ledger")

            conn = sql.connect("database.db")
            cur = conn.cursor()

            prod = cur.execute('''SELECT * from issued WHERE issuedfrom = ? AND productId = ? AND district=? AND battalion=? AND station=?''',(retrievedTo, session['productId'], district, battalion_form, station)).fetchall()


            if not prod:
                if district == '1':
                    return render_template('retrieve.html', count=1, data=stationdata, battalions=battalion,
                                       error=f'This product was not issued to {battalion_form} from {retrievedTo}')
                else:
                    return render_template('retrieve.html', count=1, data=stationdata, battalions=battalion,
                                           error=f'This product was not issued to {station} from {retrievedTo}')


            if prod[0][-1] < int(qty):
                return render_template('retrieve.html', count=1, data=stationdata, battalions=battalion,
                                       error="Retriving quantity cannot be greater than issued quantity")


            cur.execute("""INSERT INTO retrieve (retrievedBy, retrievedTo, productId, productname,  district, battalion, quantity, station, substation)
                          VALUES (?,?,?,?,?,?,?,?,?)""", (
            session['email'], retrievedTo, session['productId'],session['productname'], district, battalion_form, qty, station, substation))

            inventoryQuantity = int(session['quantity']) + int(qty)
            cur.execute("UPDATE inventory SET quantity=? WHERE uniqueId=?", (inventoryQuantity, session['productId']))
            issuedQuantity = prod[0][-1] - int(qty)
            cur.execute('UPDATE issued set quantity=? WHERE productId=?', (issuedQuantity, session['productId']))
            conn.commit()
            conn.close()

            if battalion_form == '1':
                battalion_form = "-"
            elif district == '1':
                district = "-"
                station = "-"
            data = {
                'productname': session['productname'],
                'retrievedby': session['email'],
                'district': district,
                'battalion': battalion_form,
                'station': station,
                'qty': qty,
                'substation': substation,
            }
            session.pop('productId')
            session.pop('quantity')
            return render_template('download-issued.html', **data)

        return render_template('retrieve.html', count=1, data=stationdata, battalions=battalion, error="")

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
        elif request.form['type'] == 'retrieve':
            productId = request.form['product']
            quantity = request.form['quantity']
            session['productId'] = productId
            session['quantity'] = quantity
            session['productname'] = request.form['productname']
            return redirect(url_for('retrieving'))
        elif request.form['type'] == 'assignhistory':
            conn = sql.connect("database.db")
            cur = conn.cursor()
            productname = request.form['product']
            data = cur.execute('''SELECT * FROM issued WHERE productname=?''',(productname,)).fetchall()
            return render_template('showAssignDetails.html', data = data)
        elif request.form['type'] =='retrievehistory':
            conn = sql.connect("database.db")
            cur = conn.cursor()
            productId = request.form['product']
            print(productId, file=sys.stderr)
            data = cur.execute('''SELECT * FROM retrieve WHERE productId=?''', (productId,)).fetchall()
            return render_template('showRetrieveDetails.html', data=data)
        else:
            conn = sql.connect("database.db")
            cur = conn.cursor()
            session['productId'] = request.form['product']
            # productId = request.form['product']
            # print(productId, file=sys.stderr)
            # data = cur.execute('''SELECT * FROM retrieve WHERE productId=?''', (productId,)).fetchall()
            return redirect(url_for('updateItem'))
    
    return redirect(url_for('login'))

@app.route("/edit-item", methods=["POST","GET"])
def updateItem():
    if session.get('login'):
        productId = session['productId']
        form = UpdateItemForm()
        conn = sql.connect("database.db")
        cur = conn.cursor()
        data = cur.execute('''SELECT * FROM inventory WHERE uniqueId=?''', (productId,)).fetchall()
        form.billno.data = data[0][4]
        billno = data[0][4]
        form.nameoffirm.data = data[0][5]
        nameoffirm = data[0][5]
        if form.validate_on_submit():
            addedBy = session['email']
            productname = str(request.form['productname']).lower()
            dateofsurvey = str(request.form['dateofsurvey'])
            quantity = str(request.form['quantity'])
            rateperitem = str(request.form['rateperitem'])
            totalamount = str(request.form['totalamount'])
            warranty = str(request.form['warranty'])
            conn = sql.connect("database.db")
            cur = conn.cursor()
            updatedProduct = cur.execute('''UPDATE inventory SET addedBy=?, productname=?, dateofsurvey=?, quantity=?, rateperitem=?, totalamount=?, warranty=? WHERE uniqueId=?''',(addedBy, productname, dateofsurvey, quantity, rateperitem, totalamount,warranty, productId ))
            data = {
                'productname': productname,
                'dosurvey': dateofsurvey,
                'quantity': quantity,
                'rateperitem': rateperitem,
                'totalamount': totalamount,
                'warranty': warranty
            }
            conn.commit()
            conn.close()
            return render_template('download-item.html', **data, billno=billno, nameoffirm= nameoffirm)

        form.productname.data = data[0][2]

        form.rateperitem.data = data[0][-2]
        form.warranty.data = data[0][-1]
        form.quantity.data = data[0][-4]
        conn.commit()
        conn.close()
        return render_template('updateProduct.html', form = form)
    return redirect(url_for('login'))

@app.route("/issuedto", methods=["POST","GET"])
def issuedto():
    if session.get('login'):
        issuedfrom = str(request.form.get('issuedfrom')).lower()
        district = str(request.form.get('district')).lower()
        battalion_form = str(request.form.get('battalion')).lower()
        station = str(request.form.get('station')).lower()
        substation = str(request.form.get('substation')).lower()
        qty = request.form.get('quantity')


        if issuedfrom and qty:
            if not session['productId']:
                return render_template('issuedTo.html', count=1, data=stationdata, battalions=battalion,
                                       error="Please select a product from main ledger", successMessage="")
            if int(qty) > int(session['quantity']):
                return render_template('issuedTo.html',count=1,data=stationdata,successMessage="", battalions=battalion, error = "Quantity is greater than remaining products in inventory")


            conn = sql.connect("database.db")
            cur = conn.cursor()
            cur.execute("""INSERT INTO issued (issuedBy, issuedfrom, productId, productname,  district, battalion, quantity, station, substation)
                          VALUES (?,?,?,?,?,?,?,?,?)""",(session['email'], issuedfrom, session['productId'], session['productname'],  district,battalion_form, qty, station, substation))

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
            'substation':substation,
            }
            session.pop('productId')
            session.pop('quantity')
            return render_template('download-issued.html', **data)

        return render_template('issuedTo.html',count=1 ,data=stationdata, battalions=battalion, error = "", successMessage="")

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
            warranty = str(request.form['warranty'])

            data = {
                'productname' : productname,
                'dosurvey' : dateofsurvey,
                'billno' : billno,
                'nameoffirm' : nameoffirm,
                'quantity' : quantity,
                'rateperitem' : rateperitem,
                'totalamount' : totalamount,
                'warranty':warranty
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
                nameoffirm,  quantity, rateperitem, totalamount, warranty) VALUES ( ?, ?, ?,  ?, ?, ?, ?, ?, ?,?)
                """, (id, addedBy,  productname, dateofsurvey, billno, nameoffirm, quantity, rateperitem, totalamount,warranty))
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
        
        try:
            data = cur.execute("SELECT * FROM inventory")
            data = list(data)
        except:
            data = []

        if form.validate_on_submit():

            name = str(request.form['search']).lower()
            form.search.data = ""
            if name:
                try:
                    data = cur.execute("SELECT * FROM inventory WHERE productname LIKE '%s%%' " %name)
                    data = list(data)
                    if len(data) <= 0:
                        data = cur.execute("SELECT * FROM issued WHERE station LIKE '%s%%' " %name)
                        data = list(data)
                        if(len(data) <= 0):
                            data = cur.execute("SELECT * FROM issued WHERE substation LIKE '%s%%' " %name)
                        return render_template('showAssignDetails.html', data = data)
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
        cur.execute('CREATE TABLE IF NOT EXISTS logindata (email varchar, password varchar)')
        cur.execute('''CREATE TABLE IF NOT EXISTS inventory(
            uniqueId INTEGER,
            addedBy STRING, 
            productname STRING, 
            dateofsurvey STRING, 
            billno STRING, 
            nameoffirm STRING, 
            quantity STRING, 
            rateperitem STRING, 
            totalamount STRING,
            warranty STRING)'''
        )
        cur.execute('''CREATE TABLE IF NOT EXISTS issued(
            issuedBy STRING,
            issuedfrom STRING, 
            productId STRING,
            productname STRING, 
            district STRING, 
            battalion STRING, 
            station STRING, 
            substation STRING,
            quantity STRING)'''
        )
        cur.execute('''CREATE TABLE IF NOT EXISTS retrieve(
            retrievedBy STRING,
            retrievedTo STRING, 
            productId STRING,
            productname STRING, 
            district STRING, 
            battalion STRING, 
            station STRING, 
            substation STRING,
            quantity STRING)'''
        )
        email = str(form.email.data).lower()
        password = str(form.password.data).lower()
        cur.execute('INSERT INTO logindata (email,password) VALUES (?,?)', (email, password))
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
    session['district'] = stationdata[district['name']]
    return jsonify(status="success", data=session['district'])

@app.route('/subdistrict', methods=["POST","GET"])
def subdistrict():
    data = request.get_json('district')
    session['district'] = stationdata[data['district']][data['subdistrict']]
    return jsonify(status="success", data=session['district'])
#
# @app.context_processor
# def override_url_for():
#     return dict(url_for=dated_url_for)
#
#
#
# def dated_url_for(endpoint, **values):
#     if endpoint == 'static':
#         filename = values.get('filename', None)
#         if filename:
#             file_path = os.path.join(app.root_path,
#                                  endpoint, filename)
#             values['q'] = int(os.stat(file_path).st_mtime)
#     return url_for(endpoint, **values)


@app.route('/edit', methods=["POST","GET"])
def edit():  
    conn = sql.connect("database.db")
    # conn.execute('CREATE TABLE logindata (email STRING, password STRING)')
    conn.execute('DROP TABLE IF EXISTS issued')
    cur = conn.cursor()
    conn.execute('''CREATE TABLE issued(
            issuedBy STRING,
            issuedfrom STRING, 
            productname STRING, 
            district STRING, 
            battalion STRING, 
            station STRING, 
            substation STRING, 
            quantity STRING)'''
        )
    
    # cur.execute('INSERT INTO logindata (email, password) VALUES (?,?)', ("jagmohandixit686@gmail.com", "11111111"))
    # cur.execute('INSERT INTO logindata (email, password) VALUES (?,?)', ("naiktanvi30@gmail.com", "11111111"))
    conn.commit()
    conn.close()
    return redirect(url_for('mainledger')) 
