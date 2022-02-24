from flask import Flask, render_template, url_for
import os 

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('login.html')


@app.route("/issued-to")
def issuedTo():
    return render_template('issuedTo.html')

@app.route("/add-station")
def addStation():
    return render_template('add-station.html')

@app.route('/add-item')
def addItem():
    return render_template("add-item.html")


@app.route('/main-ledger')
def mainLedger():
    return render_template("main-ledger.html")   

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
if __name__ == '__main__':
    app.run(debug=True)