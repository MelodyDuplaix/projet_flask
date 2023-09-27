# bibliothèques pour flask
from flask import Flask, render_template, request
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, SelectField, IntegerField, validators
from wtforms.validators import DataRequired
import sqlite3

# biblothèques de data
import pandas as pd

# bibliothèques de paramètrages
from dotenv import load_dotenv 

# paramètrages de lancement
load_dotenv()

# Configuration de l'app
app = Flask(__name__) # app est le nom du fichier obligatoirement, on lui attribuel l'objet Flask du nom du fichier
app.config["CACHE_TYPE"] = "null"
app.config['SECRET_KEY'] = "Ma super clé !"

# première page
@app.route("/") # méthode qui permet de créer des pages web
def f_index(): 
    return "Home" 




class t_Formulaire_enregistrement_informations(FlaskForm):
    wtf_nom = StringField("Nom*", validators=[validators.DataRequired()])
    wtf_prenom = StringField("Prenom*", validators=[validators.DataRequired()])
    wtf_type_vehicule = SelectField( "type de véhicule*", option_widget=None, validate_choice=True)
    wtf_kilometres_depart = IntegerField("nombre de kilomètres au départ*", [validators.NumberRange(min=0, max=1000000, message="Le nombre de kilomètres ne peut être négatif")])
    wtf_kilometres_fin = IntegerField("nombre de kilomètres à la fin*", [validators.NumberRange(min=0, max=1000000, message="Le nombre de kilomètres ne peut être négatif")])
    wtf_commentaire = StringField("Commentaire")
    wtf_envoyer = SubmitField("Envoyer")
    def __init__(self):
        super(t_Formulaire_enregistrement_informations, self).__init__()
        # Créez la connexion à la base de données à l'intérieur de la méthode __init__
        self.connexion = sqlite3.connect("toutroule.db")
        self.curseur = self.connexion.cursor()
        # Récupérez la liste des types de véhicules depuis la base de données
        resultats_vehicule = self.curseur.execute("SELECT DISTINCT type FROM vehicule").fetchall()
        choix_type_vehicule = [(resultat[0], resultat[0]) for resultat in resultats_vehicule]
        # Définissez les choix du champ SelectField
        self.wtf_type_vehicule.choices = choix_type_vehicule
        # Fermez le curseur (vous pouvez garder la connexion ouverte si nécessaire)
        self.curseur.close()
        



@app.route("/formulaire-saisie", methods=["GET", "POST"])
def f_formulaire_saisie(): 
    f_formulaire = t_Formulaire_enregistrement_informations()
    connexion = sqlite3.connect("toutroule.db")
    curseur = connexion.cursor()
    # table_chauffeurs = curseur.execute("SELECT nom, prenom FROM chauffeurs")
    table_chauffeurs = pd.read_sql_query("SELECT nom, prenom FROM chauffeurs", connexion)
    if f_formulaire.validate_on_submit():
        try:
            connexion = sqlite3.connect("toutroule.db")
            curseur = connexion.cursor()
            f_nom= f_formulaire.wtf_nom.data
            f_prenom= f_formulaire.wtf_prenom.data
            f_type_vehicule= f_formulaire.wtf_type_vehicule.data
            f_kilometres_depart = f_formulaire.wtf_kilometres_depart.data
            f_kilometres_fin= f_formulaire.wtf_kilometres_fin.data
            f_commentaire= f_formulaire.wtf_commentaire.data
            id_vehicule = curseur.execute(f"SELECT id_vehicule FROM vehicule WHERE type == '{f_type_vehicule}'").fetchone()[0]
            id_chauffeur = curseur.execute(f"SELECT id_chauffeur FROM chauffeurs WHERE nom=='{f_nom}' and prenom=='{f_prenom}' ").fetchone()[0]
            curseur.execute("INSERT INTO trajets (km_fin,km_debut,commentaire,id_vehicule,id_chauffeur) VALUES (?, ?, ?, ?, ?)", (f_kilometres_fin, f_kilometres_depart, f_commentaire, id_vehicule, id_chauffeur))
            connexion.commit()
            f_message = "Enregistrement inscrit dans la base."
            return render_template("t_formulaire_saisie_confirmation.html",
                t_nom = f_nom, t_prenom=f_prenom, t_type_vehicule=f_type_vehicule, t_kilometres_depart = f_kilometres_depart, t_kilometres_fin = f_kilometres_fin, 
                t_commentaire = f_commentaire, t_id_vehicule = id_vehicule, t_id_chauffeur = id_chauffeur, t_message = f_message)
        except:
            connexion.rollback()
            f_message = "Un problème est survenu pendant l'enregistrement."
            return render_template("t_formulaire_saisie_confirmation.html", t_message = f_message)
        finally:
            connexion.close()
    return render_template("t_formulaire_saisie.html" ,
                            t_titre = "Formulaire de saisie",
                            html_formulaire = f_formulaire) 


class c_ajout_salarie(FlaskForm):
  wtf_nom = StringField("Nom", validators=[DataRequired()])
  wtf_prenom = StringField("Prénom", validators=[DataRequired()])
  wtf_genre = SelectField("Genre", choices=["M","F","NB"])
  wtf_envoyer = SubmitField("Envoyer")

@app.route("/ajout-salarie", methods=["GET", "POST"])
def f_enregistrer_informations():
 f_formulaire = c_ajout_salarie()
 if f_formulaire.validate_on_submit():
    f_nom = f_formulaire.wtf_nom.data
    f_formulaire.wtf_nom.data = ""
    f_prenom = f_formulaire.wtf_prenom.data
    f_formulaire.wtf_prenom.data = ""
    f_genre = f_formulaire.wtf_genre.data
    f_formulaire.wtf_genre.data = ""
 return render_template("t_ajout-salarie.html" ,
                          t_titre = "Formulaire d'ajouter un salarié",
                          html_formulaire = f_formulaire)


# Liste des types de véhicules disponibles
types_vehicules = ["camion citerne", "camion frigorifique", "camion fourgon"]
# Route pour afficher le formulaire d'ajout de véhicule
@app.route('/ajout-vehicule', methods=['POST', 'GET'])
def f_ajout_vehicule():
    if request.method == 'POST':
        try:
            v_id = request.form['wtf_id']
            v_type = request.form['wtf_type']
            connexion = sqlite3.connect("toutroule.db")
            curseur = connexion.cursor()
            curseur.execute("INSERT INTO vehicule (id_vehicule, type) VALUES (?, ?)", (v_id, v_type))
            connexion.commit()
            f_message = "Enregistrement inscrit dans la base."
        except:
            connexion.rollback()
            f_message = "Un problème est survenu pendant l'enregistrement."
        finally:
            connexion.close()
            return render_template("ajout-vehicule.html", t_message=f_message)
    return render_template("ajout-vehicule.html", types_vehicules=types_vehicules)

@app.route("/visualiser-donnees")
def f_visualiser_donnees(): 
    pass 

@app.route("/supprimer")
def f_supprimer(): 
    pass 

@app.route("/modifier")
def f_modifier(): 
    pass 


@app.route("/rgpd")
def f_rgpd():
    return render_template("t_mentions_legales.html") 

@app.route("/mentions-legales")
def mentions_legales():
    return render_template("t_mentions_legales.html")