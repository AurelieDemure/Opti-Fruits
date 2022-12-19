from cs50 import SQL
from flask import Flask,render_template,request,redirect

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

@app.route('/inscription')
def inscription():
    return render_template("inscription.html")

@app.route('/connexion',methods=['GET','POST'])
def connexion():
    return render_template("connexion.html")

@app.route('/propose')
def propose():
    return render_template("propose.html")
    
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


@app.route('/profil',methods=['GET','POST'])
def profil():
    if request.form.get('Email') is None or request.form.get('Mot de passe') is None:
        return redirect('/connexion')    
    else:
        utilisateur=db.execute("SELECT * FROM utilisateur WHERE mail=? and password=?",request.form.get('Email'),request.form.get('Mot de passe'))
        propositions=db.execute("SELECT * FROM proposition WHERE pseudo=?",utilisateur[2])
        return render_template("profil.html",utilisateur=utilisateur,propositions=propositions)
