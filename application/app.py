from cs50 import SQL
from flask import Flask, render_template,g

db= SQL('sqlite:///Documents_Appli/bd.db')

app=Flask(__name__)



@app.route('/')
def homeDev():
    return render_template('homeDev.html')

@app.route('/testLayout')
def testLayout():
    return render_template("testLayout.html")

@app.route('/associations')
def assos():
    assos=db.execute("SELECT * FROM association ORDER BY ville")
    return render_template("Assos.html",assos=assos)