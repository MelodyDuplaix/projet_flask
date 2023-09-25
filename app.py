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
