from cs50 import SQL
from flask import Flask, render_template,g

db= SQL('sqlite:///static/bd.db')

app=Flask(__name__)



@app.route('/')
def homeDev():
    return render_template('homeDev.html')

@app.route('/testLayout')
def testLayout():
    return render_template("testLayout.html")


@app.route('/inscription')
def inscription():
    return render_template("inscription.html")

@app.route('/connexion')
def connexion():
    return render_template("connexion.html")

@app.route('/map')
def map():
    return render_template("map.html")

@app.route('/associations')
def assos():
    assos=db.execute("SELECT * FROM association ORDER BY ville")
    return render_template("Assos.html",assos=assos)

@app.route('/TODO')
def todo():
    return render_template("TODO.html")

