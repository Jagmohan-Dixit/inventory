from click import password_option
from flask import Flask, redirect, render_template, request, url_for, jsonify, session
import os 
import sqlite3 as sql
from inventory.forms import LoginForm, AdditemForm, IssuedForm, SearchForm

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def home():
    if session.get('login'):
        return redirect(url_for('mainledger'))

    return render_template('home.html')

@app.route("/login", methods=["POST","GET"])
def login():
    if session.get('login') == None:
        form = LoginForm()
        if form.validate_on_submit():
            email = request.form['email']
            password = request.form['password']

            conn = sql.connect('database.db')
            cur = conn.cursor()
            data = cur.execute('SELECT * FROM logindata WHERE email = ?', (email,))
            data = list(data)
            print("Email : ",data[0][0])
            print("Password : ",data[0][1])
            if data and str(data[0][0]) == email and str(data[0][1]) == password:
                session['login'] = True
                return redirect(url_for('mainledger'))
        
        return render_template('login.html', form=form)

    return redirect(url_for('mainledger'))


@app.route('/logout')
def logout():
    if session.get('login'):
        session.pop('login', None)
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route("/issuedto", methods=["POST","GET"])
def issuedto():
    if session.get('login'):
        form = IssuedForm()

        if form.validate_on_submit():
            issuedfrom = request.form['issuedfrom']
            issuedto = request.form['issuedto']
            district = request.form['district']

            conn = sql.connect("database.db")
            cur = conn.cursor()
            cur.execute("""INSERT INTO issued (issuedfrom, issuedto, district)
                    VALUES (?,?,?)""", (issuedfrom, issuedto, district))

            print("Data Added Successfully") 
            data = cur.execute()

        return render_template('issuedTo.html', form=form)

    return redirect(url_for('login'))

@app.route("/addstation")
def addstation():
    if session.get('login'):
        return render_template('add-station.html')

    return redirect(url_for('login'))

@app.route('/additem', methods=["POST","GET"])
def additem():
    if session.get('login'):

        form = AdditemForm()
        if form.validate_on_submit():
            issuedfrom = str(request.form['issuedfrom'])
            productname = str(request.form['productname'])
            date = str(request.form['date'])
            dateofsurvey = str(request.form['dateofsurvey'])
            billno = str(request.form['billno'])
            nameoffirm = str(request.form['nameoffirm'])
            itemno = str(request.form['itemno'])
            quantity = str(request.form['quantity'])
            rateperitem = str(request.form['rateperitem'])
            totalamount = str(request.form['totalamount'])
            crvno = str(request.form['crvno'])

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("""INSERT INTO inventory (issuedfrom, productname,date, dateofsurvey, billno, 
                nameoffirm,itemno, quantity, rateperitem, totalamount, crvno) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (issuedfrom, productname,date, dateofsurvey, billno, nameoffirm,itemno, quantity, rateperitem, totalamount, crvno))
                
                print("Data Added Successfully") 
            
            con.commit()
            return redirect(url_for('mainledger'))

        return render_template("add-item.html", form=form)
    return redirect(url_for('login'))

@app.route('/getdata', methods=["POST","GET"])
def get():
    con = sql.connect("database.db")
    # con.row_factory = sql.Row
   
    cur = con.cursor()
    cur.execute("select * from inventory")
   
    rows = cur.fetchall(); 

    return jsonify(list(rows))
    return render_template('getdata.html', data=rows)


@app.route('/mainledger', methods=["POST","GET"])
def mainledger():
    if session.get('login'):
        form = SearchForm()
        return render_template("main-ledger.html", form=form)   

    return redirect(url_for('login'))

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