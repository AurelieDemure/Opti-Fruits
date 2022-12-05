from cs50 import SQL
from flask import Flask,render_template,request

db= SQL('sqlite:///bd.db')

app=Flask(__name__,
    static_folder="./static",
    template_folder="./templates")


@app.route('/',methods=['GET','POST'])
def homeDev():
    if request.method=='GET':
        navbar='unconnectedLayout'
    if request.method=='POST':
        navbar='connectedLayout'
    return render_template('home.html',navbar=navbar)

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
    print(request)
    if request.args.get('q') is not None:
        assos=db.execute("SELECT * FROM association WHERE ville LIKE ? ORDER BY ville", "%" +request.args.get("q")+"%")
    else:
        assos=db.execute("SELECT * FROM association ORDER BY ville")
    return render_template("Assos.html",assos=assos)

@app.route('/TODO')
def todo():
    return render_template("TODO.html")

@app.route('/register')
def register():
    nom=request.form.get("nom")
    if not nom:
        return render_template("failure.html", message="Un ou plusieurs champs n'ont pas été remplis, nous ne pouvons pas vous authentifier")
