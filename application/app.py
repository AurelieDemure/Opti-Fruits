from flask import Flask, render_template

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