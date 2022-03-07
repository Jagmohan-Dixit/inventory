from flask import Flask, redirect, render_template, request, json, flash, url_for, jsonify, session, send_file
from mailmerge import MailMerge
import sqlite3 as sql
from Inventory.forms import LoginForm, AdditemForm, SearchForm, RegisterForm
import pandas as pd
import sys, os, random
from docx2pdf import convert
import pythoncom
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
            productname = request.form['product']
            quantity = request.form['quantity']
            session['productname'] = productname
            session['quantity'] = quantity
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
        print(f"battalions: {battalion_form}",file=sys.stderr)
        print(f"districts: {district}",file=sys.stderr)
        station = request.form.get('station')
        qty = request.form.get('quantity')

        if issuedfrom and qty:
            if not session['productname']:
                return render_template('issuedTo.html', count=1, data=stationdata, battalions=battalion,
                                       error="Please select a product from main ledger", successMessage="")
            if qty > session['quantity']:
                return render_template('issuedTo.html',count=1,data=stationdata,successMessage="", battalions=battalion, error = "Quantity is greater than remaining products in inventory")


            conn = sql.connect("database.db")
            cur = conn.cursor()
            cur.execute("""INSERT INTO issued (issuedBy, issuedfrom, productname,  district, battalion, quantity, station)
                          VALUES (?,?,?,?,?,?,?)""",(session['email'], issuedfrom, session['productname'],  district,battalion_form, qty, station))

            quantity = int(session['quantity']) - int(qty)
            cur.execute("UPDATE inventory SET quantity=? WHERE productname=?", (quantity, session['productname'],))
            conn.commit()
            conn.close()

            dir_path = os.path.dirname(os.path.realpath(__file__))

            pythoncom.CoInitialize()
            new_file_path = os.path.join(dir_path, 'issued_template.docx')
            document = MailMerge(new_file_path)
            if battalion_form == '1':
                battalion_form = "-"
            elif district == '1':
                district = "-"
                station = "-"
            document.merge(
            productname= session['productname'],
            issuedBy = session['email'],
            district = district,
            battalion = battalion_form,
            station = station,
            qty=qty,
            )
            document.write(os.path.join(dir_path, 'output.docx'))
            #convert(os.path.join(dir_path, 'output.docx'), os.path.join(dir_path, 'output.pdf'))
            session.pop('productname')
            session.pop('quantity')
            return render_template('issuedTo.html', count=1, data=stationdata, battalions=battalion, error="",
                                   successMessage="Product Issued successfully!")

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

            pythoncom.CoInitialize()
            dir_path = os.path.dirname(os.path.realpath(__file__))
            new_file_path = os.path.join(dir_path, 'item_template.docx')
            document = MailMerge(new_file_path)
            document.merge(
                productName = productname,
                dosurvey = dateofsurvey,
                billno = billno,
                nameoffirm = nameoffirm,
                quantity = quantity,
                rateperitem = rateperitem,
                totalamount = totalamount
            )

            document.write(os.path.join(dir_path, 'item.docx'))
            #convert(os.path.join(dir_path,  'output.docx'), os.path.join(dir_path, 'output.pdf'))

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
            form= AdditemForm(formdata=None)
            # form.productname.data = ""
            # form.dateofsurvey.raw_data = ["yyyy-mm-dd"]
            # form.billno.data  =""
            # form.nameoffirm.data  = ""
            # form.quantity.raw_data  = 0
            # form.rateperitem.data  = ""
            # form.totalamount.data  = ""
            return render_template("add-item.html", form=form, successMessage="Item Added Successfully!")

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
            print(name)
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
        print(f'data: {data}', file=sys.stderr)
        return render_template("main-ledger.html", form=form, data=data, error = "")

    return redirect(url_for('login'))    



@app.route('/download', methods=["POST","GET"])
def download():
    con = sql.connect("database.db")
    if request.form['type'] == "excel":
        try:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            new_file_path = os.path.join(dir_path, 'data.xlsx')
            filepath = open(new_file_path, 'wb')
            writer = pd.ExcelWriter(filepath, engine='xlsxwriter')

            # creating a dataframe
            df = pd.read_sql("SELECT * FROM inventory", con)

            print(type(df), file=sys.stderr)
            df.to_excel(writer, sheet_name='inventory', index=False)
            writer.save()
            return send_file('data.xlsx', as_attachment=True)
        except:
            return redirect(url_for('mainledger', error ="Unable to download excel file"))

@app.route('/register', methods = ['POST','GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        con = sql.connect("database.db")
        cur = con.cursor()

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
