# bibliothèques pour flask
from flask import Flask, flash, render_template, request, redirect
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, SelectField, IntegerField, validators
from wtforms.validators import DataRequired
import sqlite3
from lib.utils import *
from lib.database import *
from lib.analyses import *

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
    df= requetes_tables_transformation_dataframe()
    v_afficher_nombres_chauffeurs = afficher_nombre_chauffeurs(df)
    v_afficher_nom_prenom = afficher_nom_prenom_chauffeurs(df)
    v_nb_de_km_parcouru_total = nb_de_km_parcouru_total(df)
    v_graphique = graphique(df)
    return render_template("t_analyses.html", t_afficher_nombres_chauffeurs = v_afficher_nombres_chauffeurs,
                                        t_afficher_nom_prenom = v_afficher_nom_prenom,
                                        t_nb_de_km_parcouru_total = v_nb_de_km_parcouru_total,
                                        t_graphique = v_graphique)









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











@app.route('/supprimer-vehicule', methods=['POST', 'GET'])
def supprimer_vehicule():
    f_message = ""
    types_vehicules = []
    try:
        connexion = sqlite3.connect("toutroule.db")
        curseur = connexion.cursor()
        # Récupérer tous les types de véhicules
        curseur.execute("SELECT DISTINCT type FROM vehicules")
        types_vehicules = [row[0] for row in curseur.fetchall()]
    except Exception as e:
        print(str(e))
    finally:
        connexion.close()
    if request.method == 'POST':
        type_choisi = request.form.get('type_choisi')
        if type_choisi:
            try:
                connexion = sqlite3.connect("toutroule.db")
                curseur = connexion.cursor()
                # Supprimer le véhicule en fonction du type choisi
                curseur.execute("DELETE FROM vehicules WHERE type=?", (type_choisi,))
                connexion.commit()
                f_message = "Véhicule(s) supprimé(s) avec succès."
            except Exception as e:
                print(str(e))
                connexion.rollback()
                f_message = "Un problème est survenu lors de la suppression du véhicule."
            finally:
                connexion.close()
    return render_template("t_supprimer_vehicule.html", t_titre="Supprimer un type de véhicule", t_message=f_message, types_vehicules=types_vehicules)


# Formulaire de recherche
class SearchForm(FlaskForm):
    nom = StringField('Saisissez le nom du salarié', validators=[DataRequired()])
    submit_search = SubmitField('Rechercher')
# Formulaire de suppression
class DeleteForm(FlaskForm):
    submit_delete = SubmitField('Supprimer')

@app.route('/supprimer-salarie', methods=['GET', 'POST'])
def supprimer_salarie():
    search_form = SearchForm()
    delete_form = DeleteForm()
    if search_form.validate_on_submit():
        nom = search_form.nom.data
        salarie_data = search_salarie(nom)
        return render_template('t_supprimer_salarie.html', search_form=search_form, delete_form=delete_form, salarie_data=salarie_data)
    if delete_form.validate_on_submit():
        selected_id = request.form['selected_id']
        delete_salarie(selected_id)
        flash("Le salarié a été supprimé.", 'success')
    return render_template('t_supprimer_salarie.html', search_form=search_form, delete_form=delete_form, salarie_data=None)











# class pour contrôler le formulaire d'ajout de salarié
class c_modifier_salarie_nom(FlaskForm):
    # Liste des types de véhicules disponibles
    wtf_nom = StringField("Nom", validators=[DataRequired()])
    wtf_prenom = StringField("Prénom", validators=[DataRequired()])
    wtf_envoyer = SubmitField("Envoyer")

@app.route("/modifier-chauffeur", methods=['POST', 'GET'])
def f_modifier(): 
    f_formulaire = c_modifier_salarie_nom()
    if f_formulaire.validate_on_submit():
        f_nom = f_formulaire.wtf_nom.data
        f_prenom = f_formulaire.wtf_prenom.data
        return redirect(f'/modifier/{f_nom}-{f_prenom}')
    return render_template("t_table_modifier_chauffeur.html", html_formulaire = f_formulaire)
    





class c_modifier_donnees_salarie(FlaskForm):
    # Liste des types de véhicules disponibles
    wtf_nom = StringField("Nom", validators=[DataRequired()])
    wtf_prenom = StringField("Prénom", validators=[DataRequired()])
    wtf_genre = SelectField("Genre", choices=["M","F","NB"])
    wtf_envoyer = SubmitField("Envoyer")


@app.route("/modifier/<nom_chauffeur>", methods=['POST', 'GET'])
def nom_chauffeur(nom_chauffeur):
    f_nom_initial = nom_chauffeur.split("-")[0]
    f_prenom_initial = nom_chauffeur.split("-")[1]
    f_formulaire = c_modifier_donnees_salarie()
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
            curseur.execute("UPDATE chauffeurs SET nom=?, prenom=?, genre=? WHERE nom=? and prenom=?", (f_nom, f_prenom, f_genre, f_nom_initial,f_prenom_initial))
            connexion.commit()
            f_message = "Modification inscrit dans la base."
        except Exception as e:
            print(str(e))
            connexion.rollback()
            return "Un problème est survenu pendant l'enregistrement."
        finally:
            connexion.close()
    return render_template("t_modifier_donnees_chauffeur.html", html_formulaire = f_formulaire)


    
    
    
    
    
    
    
    
    
# Class pour modifier les véhicules
class c_modifier_vehicule(FlaskForm):
    wtf_type = SelectField("Type de véhicule", validators=[DataRequired()])
    wtf_nouveau_type = StringField("Nouveau type de véhicule", validators=[DataRequired()])
    wtf_envoyer = SubmitField("Envoyer")
    def __init__(self):
        super(c_modifier_vehicule, self).__init__()
        # Créez la connexion à la base de données à l'intérieur de la méthode __init__
        self.connexion = sqlite3.connect("toutroule.db")
        self.curseur = self.connexion.cursor()
        # Récupérez la liste des types de véhicules depuis la base de données
        f_vehicules = self.curseur.execute("SELECT DISTINCT type FROM vehicules").fetchall()
        # Définissez les choix du champ SelectField
        self.wtf_type.choices = [(resultat[0], resultat[0]) for resultat in f_vehicules]
        # Fermez le curseur (vous pouvez garder la connexion ouverte si nécessaire)
        self.curseur.close()
@app.route("/modifier_vehicule", methods=['POST', 'GET'])
def f_modifier_vehicule():
    f_formulaire = c_modifier_vehicule()
    if f_formulaire.validate_on_submit():
        ancien_type = f_formulaire.wtf_type.data
        nouveau_type = f_formulaire.wtf_nouveau_type.data
        try:
            connexion = sqlite3.connect("toutroule.db")
            curseur = connexion.cursor()
            # Effectuer la mise à jour en utilisant les valeurs fournies dans le formulaire
            curseur.execute("UPDATE vehicules SET type=? WHERE type=?", (nouveau_type, ancien_type))
            connexion.commit()
            return "Mise à jour réussie"
        except Exception as e:
            print(str(e))
            connexion.rollback()
            return "Un problème est survenu lors de la mise à jour"
        finally:
            connexion.close()
    return render_template("t_modifier_vehicule.html", html_formulaire=f_formulaire)













@app.route("/rgpd")
def f_rgpd():
    return render_template("t_rgpd.html") 

@app.route("/mentions-legales")
def mentions_legales():
    return render_template("t_mentions_legales.html")

@app.errorhandler (404) 
def page_introuvable(e): 
	return render_template ("t_404.html" ), 404