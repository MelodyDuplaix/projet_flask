# bibliothèques pour flask
from flask import Flask, render_template

# biblothèques de data
import pandas as pd

# bibliothèques de paramètrages
from dotenv import load_dotenv 

# paramètrages de lancement
load_dotenv()

# Configuration de l'app
app = Flask(__name__) # app est le nom du fichier obligatoirement, on lui attribuel l'objet Flask du nom du fichier
app.config["CACHE_TYPE"] = "null"

# première page
@app.route("/") # méthode qui permet de créer des pages web
def f_index(): 
    return "" 


@app.route("/formulaire-saisie")
def f_formulaire_saisie(): 
    pass 

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