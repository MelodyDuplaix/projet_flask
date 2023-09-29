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

def recuperer_table_trajets():
    connexion = sqlite3.connect("toutroule.db")
    table_trajets = pd.read_sql_query("SELECT * FROM trajets", connexion)
    connexion.commit()
    connexion.close()
    return table_trajets


# Fonction pour effectuer la recherche
def search_salarie(nom):
    connexion = sqlite3.connect('toutroule.db')
    curseur = connexion.cursor()
    # Recherche des salariés par nom
    curseur.execute("SELECT id_chauffeur, nom, prenom FROM chauffeurs WHERE nom LIKE ?", ('%' + nom + '%',))
    salarie_data = curseur.fetchall()
    connexion.close()
    return salarie_data
# Fonction pour supprimer un salarié
def delete_salarie(id_chauffeur):
    connexion = sqlite3.connect('toutroule.db')
    curseur = connexion.cursor()
    # Suppression du salarié
    curseur.execute("DELETE FROM chauffeurs WHERE id_chauffeur=?", (id_chauffeur,))
    connexion.commit()
    connexion.close()