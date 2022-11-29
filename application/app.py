from flask import Flask, render_template

app=Flask(__name__)

@app.route('/')
def homeDev():
    return render_template('homeDev.html')

@app.route('/testLayout')
def testLayout():
    return render_template("testLayout.html")

@app.route('/map')
def map():
    return render_template("map.html")

