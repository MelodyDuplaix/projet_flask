# bibliothèques pour flask
from flask import Flask, render_template, request
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, SelectField, IntegerField, validators, ValidationError
from wtforms.validators import DataRequired
import sqlite3
from lib.utils import *
from lib.database import *

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
        resultats_vehicule = self.curseur.execute("SELECT DISTINCT type FROM vehicules").fetchall()
        choix_type_vehicule = [(resultat[0], resultat[0]) for resultat in resultats_vehicule]
        # Définissez les choix du champ SelectField
        self.wtf_type_vehicule.choices = choix_type_vehicule
        # Fermez le curseur (vous pouvez garder la connexion ouverte si nécessaire)
        self.curseur.close()
        

@app.route("/formulaire-saisie", methods=["GET", "POST"])
def f_formulaire_saisie(): 
    f_formulaire = t_Formulaire_enregistrement_informations()
    table_chauffeurs = recuperation_chauffeurs()
    if f_formulaire.validate_on_submit():
        try:
            f_nom= f_formulaire.wtf_nom.data
            f_prenom= f_formulaire.wtf_prenom.data
            f_type_vehicule= f_formulaire.wtf_type_vehicule.data
            f_kilometres_depart = f_formulaire.wtf_kilometres_depart.data
            f_kilometres_fin= f_formulaire.wtf_kilometres_fin.data
            f_commentaire= f_formulaire.wtf_commentaire.data
            id_vehicule = recuperation_id_vehicule(f_type_vehicule)
            id_chauffeur = recuperation_id_chauffeur(f_nom, f_prenom)
            envoie_donnees_chauffeur(f_kilometres_fin, f_kilometres_depart,f_commentaire,id_vehicule,id_chauffeur)
            f_message = "Enregistrement inscrit dans la base."
            return render_template("t_formulaire_saisie_confirmation.html",
                t_nom = f_nom, t_prenom=f_prenom, t_type_vehicule=f_type_vehicule, t_kilometres_depart = f_kilometres_depart, t_kilometres_fin = f_kilometres_fin, 
                t_commentaire = f_commentaire, t_id_vehicule = id_vehicule, t_id_chauffeur = id_chauffeur, t_message = f_message)
        except:
            return "Un problème est survenu pendant l'enregistrement, vérifier que le nom est le prénom rentrés sont bien déja enregistré en tant que chauffeur."
    return render_template("t_formulaire_saisie.html" ,
                            t_titre = "Formulaire de saisie",
                            html_formulaire = f_formulaire) 







# class pour contrôler le formulaire d'ajout de salarié
class c_ajouter_salarie(FlaskForm):
    # Liste des types de véhicules disponibles
    wtf_nom = StringField("Nom", validators=[DataRequired()])
    wtf_prenom = StringField("Prénom", validators=[DataRequired()])
    wtf_genre = SelectField("Genre", choices=["M","F","NB"])
    wtf_envoyer = SubmitField("Envoyer")

 # # Route pour afficher le formulaire d'ajout de salarié
@app.route('/ajouter-salarie', methods=['POST', 'GET'])
def f_ajouter_salarie():
    f_formulaire = c_ajouter_salarie()
    f_message = ""
    # transmission des données vers le formulaire
    if f_formulaire.validate_on_submit():
        f_nom = f_formulaire.wtf_nom.data
        f_formulaire.wtf_nom.data = ""
        f_prenom = f_formulaire.wtf_prenom.data
        f_formulaire.wtf_prenom.data = ""
        f_genre = f_formulaire.wtf_genre.data
        f_formulaire.wtf_genre.data = ""
        try:
            connexion = sqlite3.connect("toutroule.db")
            curseur = connexion.cursor()
            curseur.execute("INSERT INTO chauffeurs (nom, prenom, genre) VALUES (?, ?, ?)", (f_nom, f_prenom, f_genre))
            connexion.commit()
            f_message = "Enregistrement inscrit dans la base."
        except Exception as e:
            print(str(e))
            connexion.rollback()
            f_message = "Un problème est survenu pendant l'enregistrement."
        finally:
            connexion.close()
    return render_template("t_ajouter_salarie.html", t_titre="Ajouter un salarié", html_formulaire=f_formulaire)
if __name__ == "__main__":
    app.run(debug=True)






# class pour contrôler le formulaire d'ajout de véhicule
class c_ajouter_vehicule(FlaskForm):
    # Liste des types de véhicules disponibles
    wtf_type = StringField("Nouveau type de véhicule", validators=[DataRequired()])
    wtf_ajouter = SubmitField("Ajouter")
# Route pour afficher le formulaire d'ajout de véhicule
@app.route('/ajouter-vehicule', methods=['POST', 'GET'])
def f_ajouter_vehicule():
    f_formulaire = c_ajouter_vehicule()
    f_message = ""
    # transmission des données vers le formulaire
    if f_formulaire.validate_on_submit():
        f_type = f_formulaire.wtf_type.data
        f_formulaire.wtf_type.data = ""
        try:
            connexion = sqlite3.connect("toutroule.db")
            curseur = connexion.cursor()
            curseur.execute("INSERT INTO vehicules (type) VALUES (?)", (f_type,))
            connexion.commit()
            f_message = "Enregistrement inscrit dans la base."
        except Exception as e:
            print(str(e))
            connexion.rollback()
            f_message = "Un problème est survenu pendant l'enregistrement."
        finally:
            connexion.close()
    return render_template("t_ajouter_vehicule.html", t_titre="Ajouter un type de véhicule", html_formulaire=f_formulaire)
if __name__ == "__main__":
    app.run(debug=True)








@app.route("/visualiser-donnees")
def f_visualiser_donnees(): 
    df_chauffeurs = recuperer_table_chauffeur()
    taille_df_chauffeur = df_chauffeurs.shape[0]
    table_vehicule = recuperer_table_vehicule()
    taille_df_vehicule = table_vehicule.shape[0]
    return render_template("t_visualiser_donnees.html", t_chauffeurs = df_chauffeurs, t_vehicule = table_vehicule, t_taille_df_chauffeur = taille_df_chauffeur, t_taille_df_vehicule=taille_df_vehicule)




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

@app.errorhandler (404) 
def page_introuvable(e): 
	return render_template ("t_404.html" ), 404