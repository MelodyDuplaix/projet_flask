import sqlite3
import pandas as pd

def envoie_donnees_chauffeur(f_kilometres_fin, f_kilometres_depart,f_commentaire,id_vehicule,id_chauffeur ):
    connexion = sqlite3.connect("toutroule.db")
    curseur = connexion.cursor()
    curseur.execute("INSERT INTO trajets (km_fin,km_debut,commentaire,id_vehicule,id_chauffeur) VALUES (?, ?, ?, ?, ?)", (
        f_kilometres_fin, f_kilometres_depart, f_commentaire, id_vehicule, id_chauffeur))
    connexion.commit()
    connexion.close()
    
    
def recuperer_table_chauffeur():
    connexion = sqlite3.connect("toutroule.db")
    table_chauffeurs = pd.read_sql_query("SELECT * FROM chauffeurs", connexion)
    connexion.commit()
    connexion.close()
    return table_chauffeurs

def recuperer_table_vehicule():
    connexion = sqlite3.connect("toutroule.db")
    table_vehicule = pd.read_sql_query("SELECT * FROM vehicules", connexion)
    connexion.commit()
    connexion.close()
    return table_vehicule

