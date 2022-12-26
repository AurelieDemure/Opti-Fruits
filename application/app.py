import os
import sqlite3
from cs50 import SQL
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename

db= SQL('sqlite:///bd2.db')

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
    'Provence-Alpes-Côte d\'Azur': ['04', '05', '06', '13', '83', '84'],
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

@app.route('/connexion',methods=['GET','POST'])
def connexion():
    return render_template("connexion.html",message=' ')

@app.route('/connexion/<string:message>',methods=['GET','POST'])
def connexion2(message:str):
    return render_template("connexion.html",message=message)


@app.route('/inscription', methods=['GET','POST'])
def inscription():
    if request.method=='GET':
        return render_template("inscription.html")
    if request.method=='POST':
        nom = request.form.get("nom")
        prenom = request.form.get("prenom")
        pseudo = request.form.get("pseudo")
        tel = request.form.get("tel")
        mail = request.form.get("mail")
        password = request.form.get("password")
        mention = request.form.get("mention")
        if not nom :
            return render_template("inscription.html", message='Veuillez renseigner votre nom', nom=nom, prenom=prenom, pseudo=pseudo, tel=tel, mail=mail, password=password, mention=mention)
        if not prenom :
            return render_template("inscription.html", message='Veuillez renseigner votre prénom', nom=nom, prenom=prenom, pseudo=pseudo, tel=tel, mail=mail, password=password, mention=mention)
        if not pseudo :
            return render_template("inscription.html", message='Veuillez renseigner votre pseudo', nom=nom, prenom=prenom, pseudo=pseudo, tel=tel, mail=mail, password=password, mention=mention)
        if not tel :
            return render_template("inscription.html", message='Veuillez renseigner votre numéro de téléphone', nom=nom, prenom=prenom, pseudo=pseudo, tel=tel, mail=mail, password=password, mention=mention)
        if not mail :
            return render_template("inscription.html", message='Veuillez renseigner votre adresse mail', nom=nom, prenom=prenom, pseudo=pseudo, tel=tel, mail=mail, password=password, mention=mention)
        if not password :
            return render_template("inscription.html", message='Veuillez renseigner votre mot de passe', nom=nom, prenom=prenom, pseudo=pseudo, tel=tel, mail=mail, password=password, mention=mention)
        connection = sqlite3.connect('bd2.db')
        connection.execute("INSERT INTO utilisateur(nom,prenom,pseudo,tel,mail,password,mention) VALUES('" +nom+ "', '" +prenom+"', '" +pseudo+"', '" +tel+"', '" +mail+"', '" +password+"', '" +mention+"')")
        connection.commit()
        connection.close()
        return render_template("profil.html")
       
        




@app.route('/map')
def map():
    return render_template("map.html")

@app.route('/profil',methods=['GET','POST'])
def profil():
    if request.form['Email']=='':
        return redirect('/connexion/Veuillez renseigner votre adresse mail')    
    elif request.form['Mot de passe']=='':
        return redirect('/connexion/Veuillez rentrer votre mot de passe')
    else:
        utilisateur1=db.execute("SELECT * FROM utilisateur WHERE mail==?",request.form['Email'])
        utilisateur2=db.execute("SELECT * FROM utilisateur WHERE password==?",request.form['Mot de passe'])
        if utilisateur1!=utilisateur2:
             return redirect('/connexion/Adresse mail ou mot de passe incorrect')
        else:
            propositions=db.execute("SELECT * FROM proposition WHERE pseudo=?",utilisateur1[2])            
            return render_template("profil.html",utilisateur=utilisateur1,propositions=propositions)


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

@app.route('/recherche', methods=['GET','POST'])
def recherche():
    return render_template('recherche.html', departements=DEPARTEMENTS)

@app.route('/recherche/cp<int:codepostal>',methods=['GET','POST'])
def recherchecp(codepostal:int):
    propositions = db.execute("SELECT * FROM proposition WHERE codepostal LIKE ? ORDER BY ville")
    return render_template('recherchercp', propositions=propositions)

@app.route('/TODO')
def todo():
    return render_template("TODO.html")