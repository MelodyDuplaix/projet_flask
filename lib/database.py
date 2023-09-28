import sqlite3

def envoie_donnees_chauffeur(f_kilometres_fin, f_kilometres_depart,f_commentaire,id_vehicule,id_chauffeur ):
    connexion = sqlite3.connect("toutroule.db")
    curseur = connexion.cursor()
    curseur.execute("INSERT INTO trajets (km_fin,km_debut,commentaire,id_vehicule,id_chauffeur) VALUES (?, ?, ?, ?, ?)", (
        f_kilometres_fin, f_kilometres_depart, f_commentaire, id_vehicule, id_chauffeur))
    connexion.commit()
    connexion.close()