from flask import Flask, redirect, render_template, request, json, flash, url_for, jsonify, session, send_file
from mailmerge import MailMerge
import sqlite3 as sql
from Inventory.forms import LoginForm, AdditemForm, SearchForm
import pandas as pd
import sys,os
from docx2pdf import convert
from Inventory.data import district, stationdata, battalion

app = Flask(__name__)

app.config['SECRET_KEY'] = "mysecretkey"

# @app.route('/')
# def home():
#     if session.get('login'):
#         flash("You are Logged In")
#         return redirect(url_for('mainledger'))
#
#     flash("You are Not Logged In")
#     return render_template('login.html')



@app.route("/", methods=["POST","GET"])
def login():
    if session.get('login') == None:
        form = LoginForm()
        if form.validate_on_submit():
            email = request.form['email']
            password = request.form['password']

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
            print("issuing", file=sys.stderr)
            productname = request.form['product']
            quantity = request.form['quantity']
            session['productname'] = productname
            session['quantity'] = quantity
            print(productname)
            return redirect(url_for('issuedto'))
        else:
            conn = sql.connect("database.db")
            cur = conn.cursor()
            productname = request.form['product']
            data = cur.execute('''SELECT * FROM issued WHERE productname=?''',(productname,)).fetchall()

            print(data, file=sys.stderr)
            return render_template('showAssignDetails.html', data = data)
    
    return redirect(url_for('login'))
#
# @app.route('/assigned-history')
# def showAssignedHistory():
#     if session.get('login'):
#         productname = request.form['product']
#         print(productname, file=sys.stderr)
#         return redirect(url_for('issuedto'))
#     return redirect(url_for('login'))


@app.route("/issuedto", methods=["POST","GET"])
def issuedto():
    if session.get('login'):

        issuedfrom = request.form.get('issuedfrom')
        issuedto = request.form.get('issuedto')
        district = request.form.get('district')
        station = request.form.get('station')
        qty = request.form.get('quantity')

        if district:
            print(district)

        if issuedfrom and issuedto and district and qty and district and station:
            conn = sql.connect("database.db")
            cur = conn.cursor()
            cur.execute("""INSERT INTO issued (issuedfrom, productname, issuedto, district, quantity, station)
                VALUES (?,?,?,?,?,?)""", (issuedfrom, session['productname'], issuedto, district, qty, station))
 
            quantity = int(session['quantity']) - int(qty)
            cur.execute("UPDATE inventory SET quantity=? WHERE productname=?", (quantity, session['productname'],))
            conn.commit()
            conn.close()
            session.pop('productname')
            session.pop('quantity')
            return redirect(url_for('mainledger'))

        return render_template('issuedTo.html',count=1,data=stationdata, battalions=battalion)

    return redirect(url_for('login'))

# @app.route("/addstation",  methods=["POST","GET"])
# def addstation():
#     if session.get('login'):
#         form = AddStation()
#         conn = sql.connect('database.db')
#         cur = conn.cursor()
#         data = cur.execute('SELECT * FROM district').fetchall()
#         for item in data:
#             val = str(item[0])
#             distname = item[1]
#             form.district.choices += [(val, distname)]
#         print(form.form_errors, file=sys.stderr)
#
#         if form.validate_on_submit():
#             print(form.district.data, file=sys.stderr)
#             cur.execute('''INSERT INTO policestation (psname, districtId) VALUES (?,?)''', (form.station.data, form.district.data))
#             flash('Station added successfully')
#             conn.commit()
#             conn.close()
#             return redirect(url_for('mainledger'))
#
#         conn.close()
#         return render_template('showAssignDetails.html', form = form)
#
#     return redirect(url_for('login'))

@app.route('/additem', methods=["POST","GET"])
def additem():
    if session.get('login'):

        form = AdditemForm()
        if form.validate_on_submit():

            issuedfrom = str(request.form['issuedfrom']).lower()
            productname = str(request.form['productname']).lower()
            date = str(request.form['date'])
            dateofsurvey = str(request.form['dateofsurvey'])
            billno = str(request.form['billno']).lower()
            nameoffirm = str(request.form['nameoffirm']).lower()
            itemno = str(request.form['itemno'])
            quantity = str(request.form['quantity'])
            rateperitem = str(request.form['rateperitem'])
            totalamount = str(request.form['totalamount'])
            crvno = str(request.form['crvno']).lower()
            dir_path = os.path.dirname(os.path.realpath(__file__))
            new_file_path = os.path.join(dir_path, 'item_template.docx')
            template = 'item_template.docx'
            document = MailMerge(new_file_path)
            document.merge(
                issuedfrom = issuedfrom,
                productName = productname,
                date = date,
                dosurvey = dateofsurvey,
                billno = billno,
                nameoffirm = nameoffirm,
                itemno = itemno,
                quantity = quantity,
                rateperitem = rateperitem,
                totalamount = totalamount,
                crvno = crvno
            )
            document.write(os.path.join(dir_path, 'output.docx'))
            convert(os.path.join(dir_path, 'output.docx'),os.path.join(dir_path, 'output.pdf'))
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("""INSERT INTO inventory (issuedfrom, productname,date, dateofsurvey, billno, 
                nameoffirm,itemno, quantity, rateperitem, totalamount, crvno) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (issuedfrom, productname,date, dateofsurvey, billno, nameoffirm,itemno, quantity, rateperitem, totalamount, crvno))
                session['productname'] = productname
                flash("Data Added Successfully")
                print("Data Added Successfully") 
            
            con.commit()
            con.close()
            return send_file('output.pdf', as_attachment=True)

        return render_template("add-item.html", form=form)
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
