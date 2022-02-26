from flask import Flask, redirect, render_template, request, flash, url_for, jsonify, session
import os 
import sqlite3 as sql
from Inventory.forms import LoginForm, AdditemForm, IssuedForm, SearchForm


app = Flask(__name__)

app.config['SECRET_KEY'] = "mysecretkey"


@app.route('/')
def home():
    if session.get('login'): 
        flash("You are Logged In")
        return redirect(url_for('mainledger'))

    flash("You are Not Logged In")
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
                session['email'] = email
                return redirect(url_for('mainledger'))
        
        return render_template('login.html', form=form)

    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    if session.get('login'):
        session.clear()
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/issueing', methods=["POST","GET"])
def issueing():
    if session.get('login'):
        productname = request.form['product']
        quantity = request.form['quantity']
        session['productname'] = productname
        session['quantity'] = quantity
        print(productname)
        return redirect(url_for('issuedto'))
    
    return redirect(url_for('login'))



@app.route("/issuedto", methods=["POST","GET"])
def issuedto():
    if session.get('login'):
        form = IssuedForm()

        if form.validate_on_submit():
            issuedfrom = request.form['issuedfrom']
            issuedto = request.form['issuedto']
            district = request.form['district']
            qty = request.form['quantity']

            conn = sql.connect("database.db")
            cur = conn.cursor()
            cur.execute("""INSERT INTO issued (issuedfrom, productname, issuedto, district, quantity)
                    VALUES (?,?,?,?,?)""", (issuedfrom, session['productname'], issuedto, district, qty))
 
            quantity = int(session['quantity']) - int(qty)
            cur.execute("UPDATE inventory SET quantity=? WHERE productname=?", (quantity, session['productname'],))
            conn.commit()
            conn.close()
            session.pop('productname')
            session.pop('quantity')
            flash("Assigned Successfully")
            return redirect(url_for('mainledger'))


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
            return redirect(url_for('mainledger'))

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
            data = cur.execute("SELECT * FROM inventory WHERE productname=?",(name,))
            data = list(data) 

        con.commit()
        con.close() 
        return render_template("main-ledger.html", form=form, data=data)   
    
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


# @app.route('/edit', methods=["POST","GET"])
# def edit():  
    # conn = sql.connect("database.db")
    # conn.execute('CREATE TABLE logindata (email STRING, password STRING)')
    # conn.execute('DROP TABLE IF EXISTS issued')
    # conn.execute('CREATE TABLE issued (issuedfrom STRING, productname STRING, issuedto STRING, district STRING, quantity STRING)')
    # cur = conn.cursor()
    # cur.execute('INSERT INTO logindata (email, password) VALUES (?,?)', ("jagmohandixit686@gmail.com", "11111111"))
    # cur.execute('INSERT INTO logindata (email, password) VALUES (?,?)', ("naiktanvi30@gmail.com", "11111111"))
    # conn.commit()
    # conn.close()
    # return redirect(url_for('home')) 
