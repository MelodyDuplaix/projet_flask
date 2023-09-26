# bibliothèques pour flask
from flask import Flask, render_template
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, SelectField, IntegerField, validators
from wtforms.validators import DataRequired

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
    wtf_nom = StringField( "Nom*", validators =[DataRequired()]) 
    wtf_prenom = StringField( "Prenom*", validators =[DataRequired()])
    wtf_type_vehicule = SelectField( "type de véhicule*", choices=["camion citerne", "camion benne", "camion frigorifique", "camion fourgon"], option_widget=None, validate_choice=True)
    wtf_kilometres_depart = IntegerField("nombre de kilomètres au départ*", [validators.NumberRange(min=0, max=1000000, message="Le nombre de kilomètres ne peut être négatif")])
    wtf_kilometres_fin = IntegerField("nombre de kilomètres à la fin*",[validators.NumberRange(min=0, max=1000000, message="Le nombre de kilomètres ne peut être négatif")])
    wtf_commentaire = StringField("Commentaire") 
    wtf_envoyer = SubmitField( "Envoyer" )


@app.route("/formulaire-saisie", methods=["GET", "POST"])
def f_formulaire_saisie(): 
 f_formulaire = t_Formulaire_enregistrement_informations()
 if f_formulaire.validate_on_submit():
    f_reponse_formulaire = {
        "nom":f_formulaire.wtf_nom.data,
        "prenom":f_formulaire.wtf_prenom.data,
        "type_vehicule":f_formulaire.wtf_type_vehicule.data,
        "kilometres_depart":f_formulaire.wtf_kilometres_depart.data,
        "kilometres_fin":f_formulaire.wtf_kilometres_fin.data,
        "commentaire":f_formulaire.wtf_commentaire.data
    }
    for formulaires in f_formulaire:
        formulaires.data = ""
    return render_template("t_formulaire_saisie_confirmation.html",
                           t_reponse_formulaire = f_reponse_formulaire)
 return render_template("t_formulaire_saisie.html" ,
                          t_titre = "Formulaire de saisie",
                          html_formulaire = f_formulaire) 

@app.route("/ajout-salarie")
def f_ajout_salarie(): 
    pass 

@app.route("/ajout-vehicule")
def f_ajout_vehicule(): 
    pass 

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
    pass 

@app.route("/mentions-legales")
def f_mentions_legales(): 
    pass 