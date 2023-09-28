import sqlite3
import pandas as pd

def recuperation_chauffeurs():
    connexion = sqlite3.connect("toutroule.db")
    table_chauffeurs = pd.read_sql_query("SELECT nom, prenom FROM chauffeurs", connexion)
    connexion.commit()
    connexion.close()
    return table_chauffeurs


def recuperation_id_vehicule(f_vehicule):
    connexion = sqlite3.connect("toutroule.db")
    curseur = connexion.cursor()
    id_vehicule = curseur.execute(f"SELECT id_vehicule FROM vehicules WHERE type == '{f_vehicule}'").fetchone()[0]
    connexion.commit()
    connexion.close()
    return id_vehicule

def recuperation_id_chauffeur(f_nom, f_prenom):
    connexion = sqlite3.connect("toutroule.db")
    curseur = connexion.cursor()
    id_chauffeur = curseur.execute(f"SELECT id_chauffeur FROM chauffeurs WHERE nom=='{f_nom}' and prenom=='{f_prenom}' ").fetchone()[0]
    connexion.commit()
    connexion.close()
    return id_chauffeur

