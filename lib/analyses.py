import plotly.graph_objects as go
import json
import plotly
import sqlite3

#===============================================================
#Récupérer toutes les tables

#Ajouter un champ calculé qui calcul le nom de km parcouru

def calcul_km_parcouru (df):
    df["km_parcouru"] = df["km_fin"] - df["km_debut"]
    return df

def requetes_tables_transformation_dataframe():
    con = sqlite3.connect('Tout_roule.db')
    cursor = con.cursor()
    cursor.execute('''SELECT
        c.id_chauffeur,
        c.nom,
        c.prenom,
        c.genre,
        v.id_vehicule,
        v.type,
        t.id_trajet,
        t.km_debut,
        t.km_fin,
        t.commentaire
    FROM
        trajets as t
        JOIN chauffeurs as c ON t.id_chauffeur = c.id_chauffeur
        JOIN vehicule as v ON t.id_vehicule = v.id_vehicule''')  
#===============================================================
# Récupérez toutes les lignes dans un DataFrame
    df = pd.DataFrame(cursor.fetchall(), columns=[  
        'id_chauffeur',
        'nom',
        'prenom',
        'genre',
        'id_vehicule',
        'type',
        'id_trajet',
        'km_debut',
        'km_fin',
        'commentaire'
    ])

    df = calcul_km_parcouru (df)
    
    con.close() 

    return df

#pour appeler la fonction c'est:  requetes_tables_transformation_dataframe()

#===============================================================

#Afficher le nom et le prénom des chauffeurs

def afficher_nom_prenom_chauffeurs(df):
    df_identite = df[["nom", "prenom",'genre']]
    return df_identite

#pour appeler la fonction c'est: afficher_nom_prenom_chauffeurs(df)

#===============================================================

#Calculer le nombre de salarié

def afficher_nombre_chauffeurs(df):
    return len(df['id_chauffeur'].unique())

#pour appeler la fonction c'est : afficher_nombre_chauffeurs(df)

#===============================================================
#nb de km parcouru total :

def nb_de_km_parcouru_total(df):
    return df["km_parcouru"].sum()

#===============================================================
#nb de km parcouru par camion graphique :


def graphique(df):

    df_km_parcouru = df.groupby(['type'])['km_parcouru'].sum().reset_index()


    f0ig = go.Figure([go.Bar(x=df_km_parcouru["type"], y=df_km_parcouru["km_parcouru"])])

    # Ajouter une légende
    f0ig.update_layout(legend=dict(x=0.7, y=0.9))

    # Ajouter un titre # à rajouter pour centre le titre : 
    f0ig.update_layout(title="Distance parcourue par type de véhicule",title_x=0.5)

    # Ajouter des couleurs différentes aux barres
    f0ig.update_traces(marker_color=["red", "green", "blue","yellow"])

    # Ajouter des étiquettes aux barres #à rajouter pour centrer les étiquettes : 
    f0ig.update_traces(text=df_km_parcouru["km_parcouru"],textposition="outside")

    # Changer la couleur du fond du graphique
    f0ig.update_layout(plot_bgcolor="white")
    
    graph_JSON = json.dumps(f0ig, cls=plotly.utils.PlotlyJSONEncoder)

    return graph_JSON