import os
from cs50 import SQL
from flask import Flask, render_template, request, redirect, url_for 
from werkzeug.utils import secure_filename


db= SQL('sqlite:///bd.db')

UPLOAD_FOLDER='./static/proposePictures'
ALLOWED_EXTENSIONS={'png','jpg','jpeg'}

app=Flask(__name__,
    static_folder="./static",
    template_folder="./templates")

app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

#pour verifier que le fichier selectionné est bien du bon format
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods=['GET','POST'])
def homeDev():
    if request.method=='GET':
        navbar='unconnectedLayout'
    if request.method=='POST':
        navbar='connectedLayout'
    return render_template('home.html',navbar=navbar)

@app.route('/associations')
def assos():
    print(request)
    if request.args.get('q') is not None:
        assos=db.execute("SELECT * FROM association WHERE ville LIKE ? ORDER BY ville", "%" +request.args.get("q")+"%")
    else:
        assos=db.execute("SELECT * FROM association ORDER BY ville")
    return render_template("Assos.html",assos=assos)

@app.route('/connexion')
def connexion():
    return render_template("connexion.html")

@app.route('/inscription')
def inscription():
    return render_template("inscription.html")

@app.route('/map')
def map():
    return render_template("map.html")

@app.route('/propose',methods=['GET','POST'])
def propose():
    if request.method=='GET':
        return render_template("propose.html",message='')
    if request.method=='POST':
        frume=request.form.get("frume")
        quantite=request.form.get("quantite")
        codePostal=request.form.get("codePostal")
        ville=request.form.get("ville")
        dateCueillette=request.form.get("dateCueillette")
        dateFin=request.form.get("dateFin")
        cueillette=request.form.get("cueillette")
        description=request.form.get("description")
        photo=request.files['photo']
        if not frume:
            return render_template("propose.html",message='veuillez entrer un fruit ou légume',frume=frume,quantite=quantite,codePostal=codePostal,ville=ville,dateCueillette=dateCueillette,dateFin=dateFin,description=description)
        if not quantite:
            return render_template("propose.html",message='veuillez entrer une quantité',frume=frume,quantite=quantite,codePostal=codePostal,ville=ville,dateCueillette=dateCueillette,dateFin=dateFin,description=description)
        if not codePostal:
            return render_template("propose.html",message='veuillez entrer un code postal',frume=frume,quantite=quantite,codePostal=codePostal,ville=ville,dateCueillette=dateCueillette,dateFin=dateFin,description=description)
        if not ville:
            return render_template("propose.html",message='veuillez entrez une ville',frume=frume,quantite=quantite,codePostal=codePostal,ville=ville,dateCueillette=dateCueillette,dateFin=dateFin,description=description)
        if not dateCueillette:
            return render_template("propose.html",message='veuillez entrer une date de cueillette',frume=frume,quantite=quantite,codePostal=codePostal,ville=ville,dateCueillette=dateCueillette,dateFin=dateFin,description=description)
        if not dateFin:
            return render_template("propose.html",message='veuillez entrer une date de fin',frume=frume,quantite=quantite,codePostal=codePostal,ville=ville,dateCueillette=dateCueillette,dateFin=dateFin,description=description)
        if photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template("proposition.html",frume=frume,quantite=quantite,codePostal=codePostal,ville=ville,dateCueillette=dateCueillette, dateFin=dateFin,cueillette=cueillette,description=description, photo=photo.filename)

@app.route('/register')
def register():
    nom=request.form.get("nom")
    if not nom:
        return render_template("failure.html", message="Un ou plusieurs champs n'ont pas été remplis, nous ne pouvons pas vous authentifier")

@app.route('/TODO')
def todo():
    return render_template("TODO.html")