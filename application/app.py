import os
import sqlite3
from cs50 import SQL
from flask import Flask, render_template, request, redirect, session
from werkzeug.utils import secure_filename
from flask_session import Session

db= SQL('sqlite:///bd4.db')

UPLOAD_FOLDER='./static/downloadPictures'
ALLOWED_EXTENSIONS={'png','jpg','jpeg'}

app=Flask(__name__,
    static_folder="./static",
    template_folder="./templates")

app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]='filesystem'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
Session(app)

#pour verifier que le fichier selectionné est bien du bon format
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

dbfrumes=db.execute("SELECT nomfrumes FROM frumes")
frumes=[]
for dbfrume in dbfrumes:
    frumes.append(dbfrume['nomfrumes'])

dbvilles=db.execute("SELECT nom_commune_postal FROM lieux")
villes=[]
for dbville in dbvilles:
    villes.append(dbville['nom_commune_postal'])

@app.route('/')
def homeDev():
    propositions=db.execute("SELECT p.*,u.profilphoto FROM proposition AS p JOIN utilisateur AS u ON p.pseudo=u.pseudo")
    if session.get("name"):
        navbar='connectedLayout'
        profil=db.execute("SELECT * FROM utilisateur WHERE mail=?",session.get("name"))
        if profil!=[]:
            return render_template('home.html',navbar=navbar,profil=profil,propositions=propositions)
        else:
            session["name"]=None
    navbar='unconnectedLayout'
    return render_template('home.html',navbar=navbar, propositions=propositions)

@app.route('/associations')
def assos():
    print(request)
    if request.args.get('q') is not None:
        assos=db.execute("SELECT * FROM association WHERE ville LIKE ? ORDER BY ville", "%" +request.args.get("q")+"%")
    else:
        assos=db.execute("SELECT * FROM association ORDER BY ville")
    if not session.get("name"):
        navbar='unconnectedLayout'
        return render_template("Assos.html",assos=assos,navbar=navbar)
    else:
        navbar='connectedLayout'
        profil=db.execute("SELECT * FROM utilisateur WHERE mail=?",session.get("name"))
        return render_template("Assos.html",assos=assos,navbar=navbar,profil=profil)

@app.route('/connexion',methods=['GET','POST'])
def connexion():
    if session.get("name"):
        return redirect("/")
    if request.method=='GET':
        return render_template("connexion.html")
    if request.method=='POST':
        mail=request.form.get("mail")
        password=request.form.get("password")
        if not mail : 
            return render_template("connexion.html", message="Veuillez renseigner votre adresse mail", password=password)
        if not password : 
            return render_template("connexion.html", message="Veuillez renseigner votre mot de passe", mail=mail)
        password=db.execute("SELECT password FROM utilisateur WHERE password=?",password)
        password2=db.execute("SELECT password FROM utilisateur WHERE mail=?",mail)
        if password2 == password:
            session["name"]=mail
            return redirect('/profil/'+mail)
        else:
            return render_template("connexion.html", message="Adresse mail ou mot de passe incorrect")


@app.route('/inscription', methods=['GET','POST'])
def inscription():
    if session.get("name"):
        return redirect("/")
    if request.method=='GET':
        return render_template("inscription.html")
    if request.method=='POST':
        nom = request.form.get("nom")
        prenom = request.form.get("prenom")
        pseudo = request.form.get("pseudo")
        tel = request.form.get("tel")
        mail = request.form.get("mail")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        mention = request.form.get("mention")
        profilphoto=request.files['profilphoto']
        if not nom :
            return render_template("inscription.html", message='Veuillez renseigner votre nom', nom=nom, prenom=prenom, pseudo=pseudo, tel=tel, mail=mail, password=password, confirm_password=confirm_password, mention=mention, profilphoto=profilphoto)
        if not prenom :
            return render_template("inscription.html", message='Veuillez renseigner votre prénom', nom=nom, prenom=prenom, pseudo=pseudo, tel=tel, mail=mail, password=password, confirm_password=confirm_password ,mention=mention, profilphoto=profilphoto)
        if not pseudo :
            return render_template("inscription.html", message='Veuillez renseigner votre pseudo', nom=nom, prenom=prenom, pseudo=pseudo, tel=tel, mail=mail, password=password, confirm_password=confirm_password ,mention=mention, profilphoto=profilphoto)
        if not tel :
            return render_template("inscription.html", message='Veuillez renseigner votre numéro de téléphone', nom=nom, prenom=prenom, pseudo=pseudo, tel=tel, mail=mail, password=password, confirm_password=confirm_password ,mention=mention, profilphoto=profilphoto)
        if not mail :
            return render_template("inscription.html", message='Veuillez renseigner votre adresse mail', nom=nom, prenom=prenom, pseudo=pseudo, tel=tel, mail=mail, password=password, confirm_password=confirm_password ,mention=mention, profilphoto=profilphoto)
        if not password :
            return render_template("inscription.html", message='Veuillez renseigner votre mot de passe', nom=nom, prenom=prenom, pseudo=pseudo, tel=tel, mail=mail, password=password, confirm_password=confirm_password ,mention=mention, profilphoto=profilphoto)
        if not confirm_password : 
            return render_template("inscription.html", message='Veuillez confirmer votre mot de passe', nom=nom, prenom=prenom, pseudo=pseudo, tel=tel, mail=mail, password=password, confirm_password=confirm_password, mention=mention, profilphoto=profilphoto)
        if password!=confirm_password :
            return render_template("inscription.html", message='Veuillez rentrer deux fois le même mot de passe', nom=nom, prenom=prenom, pseudo=pseudo, tel=tel, mail=mail, password=password, confirm_password=confirm_password, mention=mention, profilphoto=profilphoto)
        # if not profilphoto in ALLOWED_EXTENSIONS:
        #    return render_template("inscription.html", message='La photo doit être au format png, jpg, ou jpeg', nom=nom, prenom=prenom, pseudo=pseudo, tel=tel, mail=mail, password=password, confirm_password=confirm_password, mention=mention, profilphoto=profilphoto)
        if profilphoto and allowed_file(profilphoto.filename):
            filename = secure_filename(profilphoto.filename)
            profilphoto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            connection = sqlite3.connect('bd4.db')
            try : 
                connection = sqlite3.connect('bd4.db')
                connection.execute("INSERT INTO utilisateur(nom,prenom,pseudo,tel,mail,password,mention,profilphoto) VALUES('" +nom+ "', '" +prenom+"', '" +pseudo+"', '" +tel+"', '" +mail+"', '" +password+"', '" +mention+"', '" +filename+"')")   
            except sqlite3.IntegrityError : 
                return render_template("inscription.html", message='Ce pseudo est déjà pris', nom=nom, prenom=prenom, pseudo=pseudo, tel=tel, mail=mail, password=password, confirm_password=confirm_password, mention=mention, profilphoto=profilphoto)
        else : 
            connection = sqlite3.connect('bd4.db')
            connection.execute("INSERT INTO utilisateur(nom,prenom,pseudo,tel,mail,password,mention,profilphoto) VALUES('" +nom+ "', '" +prenom+"', '" +pseudo+"', '" +tel+"', '" +mail+"', '" +password+"', '" +mention+"', NULL)")
        connection.commit()
        # return redirect('/profil/'+mail)
        connection.close()
        session["name"]=mail
        return redirect('/profil/'+mail)

@app.route('/logout')
def logout():
    session['name']=None
    return redirect('/')

@app.route('/profil/<string:mail>')
def profil(mail:str):
    utilisateur=db.execute("SELECT nom,prenom,pseudo,mail,mention FROM utilisateur WHERE mail=?",mail)
    propositions=db.execute("SELECT * FROM proposition AS p JOIN utilisateur AS u ON p.pseudo=u.pseudo WHERE u.mail=?",mail)            
    photo_profil=db.execute("SELECT profilphoto FROM utilisateur WHERE mail=?",mail)
    if photo_profil==[{'profilphoto': None}]:
        photo_profil='images/Default.png'
    else:
        for photoprofil in photo_profil:
            photo_profil='downloadPictures/'+str(photoprofil['profilphoto'])
    if session.get("name"):
        navbar='connectedLayout'
        profil=db.execute("SELECT * FROM utilisateur WHERE mail=?",session.get("name"))
        return render_template("profil.html",utilisateur=utilisateur,photo_profil=photo_profil,propositions=propositions,navbar=navbar,profil=profil)
    navbar='unconnectedLayout'
    return render_template("profil.html",utilisateur=utilisateur,photo_profil=photo_profil,propositions=propositions,navbar=navbar)



@app.route('/propose',methods=['GET','POST'])
def propose():
    if not session.get("name"):
        return redirect("/connexion")
    navbar='connectedLayout'
    profil=db.execute("SELECT * FROM utilisateur WHERE mail=?",session.get("name"))
    maxNoProp=db.execute("SELECT max(noprop) as maxnoprop FROM proposition")
    if maxNoProp[0]["maxnoprop"]==None:
        maxNoProp[0]["maxnoprop"]=0
    noProp=int(maxNoProp[0]["maxnoprop"])+1
    if request.method=='GET':
        return render_template("propose.html",message='', noprop=noProp, navbar=navbar,profil=profil)
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
        print(description)
        if photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename="no picture"
        if not frume:
            return render_template("propose.html",message='Veuillez entrer un fruit ou légume.', noprop=noProp, frume=frume,quantite=quantite,codePostal=codePostal,ville=ville,dateCueillette=dateCueillette,dateFin=dateFin,description=description,cueillette=cueillette, photo=filename,navbar=navbar,profil=profil)
        upperfrume=frume.upper()
        if upperfrume[-1]=='S':
            upperfrume=upperfrume[:-1]
        if not upperfrume in frumes:
            return render_template("propose.html",message='Fruit ou légume inconnu.', noprop=noProp, frume=frume,quantite=quantite,codePostal=codePostal,ville=ville,dateCueillette=dateCueillette,dateFin=dateFin,description=description,cueillette=cueillette, photo=filename,navbar=navbar,profil=profil)
        if not quantite:
            return render_template("propose.html",message='Veuillez entrer une quantité.', noprop=noProp, frume=frume,quantite=quantite,codePostal=codePostal,ville=ville,dateCueillette=dateCueillette,dateFin=dateFin,description=description,cueillette=cueillette, photo=filename,navbar=navbar,profil=profil)
        if not codePostal:
            return render_template("propose.html",message='Veuillez entrer un code postal.', noprop=noProp, frume=frume,quantite=quantite,codePostal=codePostal,ville=ville,dateCueillette=dateCueillette,dateFin=dateFin,description=description,cueillette=cueillette, photo=filename,navbar=navbar,profil=profil)
        if not ville:
            return render_template("propose.html",message='Veuillez entrez une ville.', noprop=noProp, frume=frume,quantite=quantite,codePostal=codePostal,ville=ville,dateCueillette=dateCueillette,dateFin=dateFin,description=description,cueillette=cueillette, photo=filename,navbar=navbar,profil=profil)
        upperville=ville.upper()
        if not upperville in villes:
            return render_template("propose.html",message='Ville inconnu.', noprop=noProp, frume=frume,quantite=quantite,codePostal=codePostal,ville=ville,dateCueillette=dateCueillette,dateFin=dateFin,description=description,cueillette=cueillette, photo=filename,navbar=navbar,profil=profil)
        dbcps=db.execute("SELECT code_postal FROM lieux WHERE nom_commune_postal=?",upperville)
        cps=[]
        for dbcp in dbcps:
            cps.append(dbcp['code_postal'])
        if not int(codePostal) in cps:
            return render_template("propose.html",message='Ville ou code postal incorrecte.', noprop=noProp, frume=frume,quantite=quantite,codePostal=codePostal,ville=ville,dateCueillette=dateCueillette,dateFin=dateFin,description=description,cueillette=cueillette, photo=filename,navbar=navbar,profil=profil)
        if not dateCueillette:
            return render_template("propose.html",message='Veuillez entrer une date de cueillette.', noprop=noProp, frume=frume,quantite=quantite,codePostal=codePostal,ville=ville,dateCueillette=dateCueillette,dateFin=dateFin,description=description,cueillette=cueillette, photo=filename,navbar=navbar,profil=profil)
        if not dateFin:
            return render_template("propose.html",message='Veuillez entrer une date de fin.', noprop=noProp, frume=frume,quantite=quantite,codePostal=codePostal,ville=ville,dateCueillette=dateCueillette,dateFin=dateFin,description=description,cueillette=cueillette, photo=filename,navbar=navbar,profil=profil)
        if filename=="no picture":
            return render_template("propose.html",message='Veuillez mettre une photo.', noprop=noProp, frume=frume,quantite=quantite,codePostal=codePostal,ville=ville,dateCueillette=dateCueillette,dateFin=dateFin,description=description,cueillette=cueillette, photo=filename,navbar=navbar,profil=profil)
        db.execute("INSERT INTO proposition (pseudo, noprop, nomfrumes, quantite, ville, codepostal, datecueillette, cueillette, dateexpiration, description, propositionphoto) VALUES(?,?,?,?,?,?,?,?,?,?,?)", profil[0]["pseudo"], noProp, upperfrume, quantite, upperville, codePostal, dateCueillette, cueillette, dateFin, description, filename)
        return redirect ('/proposition/'+str(noProp))

@app.route("/proposition/<int:noProp>")
def proposition(noProp:int):
    proposition=db.execute("SELECT p.*,u.profilphoto FROM proposition AS p JOIN utilisateur AS u ON p.pseudo=u.pseudo WHERE noprop=?",noProp)
    if not session.get("name"):
        navbar='unconnectedLayout'
        return render_template("proposition.html", proposition=proposition,navbar=navbar)
    else:
        navbar='connectedLayout'
        profil=db.execute("SELECT * FROM utilisateur WHERE mail=?",session.get("name"))
        return render_template("proposition.html", proposition=proposition,navbar=navbar,profil=profil)

@app.route('/recherche', methods=['GET','POST'])
def recherche():
    if request.method=='GET':
        if not session.get("name"):
            navbar='unconnectedLayout'
            return render_template("recherche.html",message='',departements=DEPARTEMENTS,navbar=navbar)
        else:
            navbar='connectedLayout'
            profil=db.execute("SELECT * FROM utilisateur WHERE mail=?",session.get("name"))
            return render_template("recherche.html",message='',departements=DEPARTEMENTS,navbar=navbar,profil=profil)
    if request.method=='POST':
        codePostal=request.form.get("Code Postal")
        departement=request.form.get("Départements")
        if not codePostal and not departement:
            if not session.get("name"):
                navbar='unconnectedLayout'
                return render_template("recherche.html",message='Veuillez saisir un code postal ou choisir un département',departements=DEPARTEMENTS,navbar=navbar)
            else:
                navbar='connectedLayout'
                profil=db.execute("SELECT * FROM utilisateur WHERE mail=?",session.get("name"))
                return render_template("recherche.html",message='Veuillez saisir un code postal ou choisir un département',departements=DEPARTEMENTS,navbar=navbar,profil=profil)
        elif codePostal or departement:
            if codePostal:
                propositions = db.execute("SELECT * FROM proposition WHERE codepostal=?", codePostal)
                if not session.get("name"):
                    navbar='unconnectedLayout'
                    return render_template("rechercheResultats.html",navbar=navbar,propositions=propositions)
                else:
                    navbar='connectedLayout'
                    profil=db.execute("SELECT * FROM utilisateur WHERE mail=?",session.get("name"))
                    return render_template("rechercheResultats.html",navbar=navbar,profil=profil,propositions=propositions)
            if departement:
                key_dep = list(DEPARTEMENTS.keys())
                val_dep = list(DEPARTEMENTS.values())
                dep = key_dep[val_dep.index(departement)]
                propositions = db.execute("SELECT * FROM proposition WHERE codepostal LIKE ?", str(dep) + "%")
                if not session.get("name"):
                    navbar='unconnectedLayout'
                    return render_template("rechercheResultats.html",navbar=navbar,propositions=propositions,dep=dep)
                else:
                    navbar='connectedLayout'
                    profil=db.execute("SELECT * FROM utilisateur WHERE mail=?",session.get("name"))
                    return render_template("rechercheResultats.html",navbar=navbar,profil=profil,propositions=propositions,dep=dep)

@app.route('/recherche/<string:region>')
def rechercheregion(region:str): 
    if not session.get("name"):
        if region=="GrandEst":
            propositions = db.execute("SELECT * FROM proposition WHERE codepostal LIKE ?",(str(x)+"%" for x in [50,54]))
            navbar='unconnectedLayout'
            return render_template("rechercheResultats.html",navbar=navbar,propositions=propositions)
    else:
        if region=="GrandEst":
            propositions = db.execute("SELECT * FROM proposition WHERE codepostal LIKE ?",(str(x)+"%" for x in [50,54]))
            navbar='connectedLayout'
            profil=db.execute("SELECT * FROM utilisateur WHERE mail=?",session.get("name"))
            return render_template("rechercheResultats.html",navbar=navbar,profil=profil,propositions=propositions)


@app.route('/supprPropose/<int:id>')
def supprPropose(id:int):
    if not session.get("name"):
        redirect('/')
    else:
        profil=db.execute("SELECT * FROM utilisateur WHERE mail=?",session.get("name"))
        db.execute("DELETE FROM proposition WHERE noprop=?",id)
        return render_template('supprProp.html',profil=profil)

@app.route('/TODO')
def todo():
    if not session.get("name"):
        navbar='unconnectedLayout'
        return render_template("TODO.html",navbar=navbar)
    else:
        navbar='connectedLayout'
        profil=db.execute("SELECT * FROM utilisateur WHERE mail=?",session.get("name"))
        return render_template("TODO.html",navbar=navbar,profil=profil)



REGIONS = {
    'Auvergne-Rhône-Alpes': ['01', '03', '07', '15', '26', '38', '42', '43', '63', '69', '73', '74'],
    'Bourgogne-Franche-Comté': ['21', '25', '39', '58', '70', '71', '89', '90'],
    'Bretagne': ['35', '22', '56', '29'],
    'Centre-Val de Loire': ['18', '28', '36', '37', '41', '45'],
    'Corse': ['2A', '2B'],
    'Grand Est': ['08', '10', '51', '52', '54', '55', '57', '67', '68', '88'],
    'Guadeloupe': ['971'],
    'Guyane': ['973'],
    'Hauts-de-France': ['02', '59', '60', '62', '80'],
    'Île-de-France': ['75', '77', '78', '91', '92', '93', '94', '95'],
    'La Réunion': ['974'],
    'Martinique': ['972'],
    'Normandie': ['14', '27', '50', '61', '76'],
    'Nouvelle-Aquitaine': ['16', '17', '19', '23', '24', '33', '40', '47', '64', '79', '86', '87'],
    'Occitanie': ['09', '11', '12', '30', '31', '32', '34', '46', '48', '65', '66', '81', '82'],
    'Pays de la Loire': ['44', '49', '53', '72', '85'],
    'Prov²ence-Alpes-Côte d\'Azur': ['04', '05', '06', '13', '83', '84'],
}

DEPARTEMENTS = {
    '01': 'Ain', 
    '02': 'Aisne', 
    '03': 'Allier', 
    '04': 'Alpes-de-Haute-Provence', 
    '05': 'Hautes-Alpes',
    '06': 'Alpes-Maritimes', 
    '07': 'Ardèche', 
    '08': 'Ardennes', 
    '09': 'Ariège', 
    '10': 'Aube', 
    '11': 'Aude',
    '12': 'Aveyron', 
    '13': 'Bouches-du-Rhône', 
    '14': 'Calvados', 
    '15': 'Cantal', 
    '16': 'Charente',
    '17': 'Charente-Maritime', 
    '18': 'Cher', 
    '19': 'Corrèze', 
    '2A': 'Corse-du-Sud', 
    '2B': 'Haute-Corse',
    '21': 'Côte-d\'Or', 
    '22': 'Côtes-d\'Armor', 
    '23': 'Creuse', 
    '24': 'Dordogne', 
    '25': 'Doubs', 
    '26': 'Drôme',
    '27': 'Eure', 
    '28': 'Eure-et-Loir', 
    '29': 'Finistère', 
    '30': 'Gard', 
    '31': 'Haute-Garonne', 
    '32': 'Gers',
    '33': 'Gironde', 
    '34': 'Hérault', 
    '35': 'Ille-et-Vilaine', 
    '36': 'Indre', 
    '37': 'Indre-et-Loire',
    '38': 'Isère', 
    '39': 'Jura', 
    '40': 'Landes', 
    '41': 'Loir-et-Cher', 
    '42': 'Loire', 
    '43': 'Haute-Loire',
    '44': 'Loire-Atlantique', 
    '45': 'Loiret', 
    '46': 'Lot', 
    '47': 'Lot-et-Garonne', 
    '48': 'Lozère',
    '49': 'Maine-et-Loire', 
    '50': 'Manche', 
    '51': 'Marne', 
    '52': 'Haute-Marne', 
    '53': 'Mayenne',
    '54': 'Meurthe-et-Moselle', 
    '55': 'Meuse', 
    '56': 'Morbihan', 
    '57': 'Moselle', 
    '58': 'Nièvre', 
    '59': 'Nord',
    '60': 'Oise', 
    '61': 'Orne', 
    '62': 'Pas-de-Calais', 
    '63': 'Puy-de-Dôme', 
    '64': 'Pyrénées-Atlantiques',
    '65': 'Hautes-Pyrénées', 
    '66': 'Pyrénées-Orientales', 
    '67': 'Bas-Rhin', 
    '68': 'Haut-Rhin', 
    '69': 'Rhône',
    '70': 'Haute-Saône', 
    '71': 'Saône-et-Loire', 
    '72': 'Sarthe', 
    '73': 'Savoie', 
    '74': 'Haute-Savoie',
    '75': 'Paris', 
    '76': 'Seine-Maritime', 
    '77': 'Seine-et-Marne', 
    '78': 'Yvelines', 
    '79': 'Deux-Sèvres',
    '80': 'Somme', 
    '81': 'Tarn', 
    '82': 'Tarn-et-Garonne', 
    '83': 'Var', 
    '84': 'Vaucluse', 
    '85': 'Vendée',
    '86': 'Vienne', 
    '87': 'Haute-Vienne', 
    '88': 'Vosges', 
    '89': 'Yonne', 
    '90': 'Territoire de Belfort',
    '91': 'Essonne', 
    '92': 'Hauts-de-Seine', 
    '93': 'Seine-Saint-Denis', 
    '94': 'Val-de-Marne', 
    '95': 'Val-d\'Oise',
    '971': 'Guadeloupe', 
    '972': 'Martinique', 
    '973': 'Guyane', 
    '974': 'La Réunion', 
    '976': 'Mayotte',
}
