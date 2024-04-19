import streamlit as st
import pandas as pd
import plotly.express as px

#Charger et préparer les données
def load_data():
    # Charger les données
    data = pd.read_csv('prix-carburants.csv', sep=';')  
    data[['Latitude', 'Longitude']] = data['geom'].str.split(',', expand=True)
    data['Latitude'] = pd.to_numeric(data['Latitude'], errors='coerce')
    data['Longitude'] = pd.to_numeric(data['Longitude'], errors='coerce')
    return data[data['Région'] == 'Île-de-France']

# Chargement des données
data_ile_de_france = load_data()

# Liste des types de carburants dispo
types_carburant = data_ile_de_france['Carburant'].unique()

# Sélecteur pour choisir un type de carburant
type_carburant_choisi = st.selectbox('Choisir un type de carburant:', types_carburant)

# Filtrage des données pour le type de carburant sélectionné
data_filtrée = data_ile_de_france[data_ile_de_france['Carburant'] == type_carburant_choisi]

# Titre de la page
st.title('Carte des Stations-Service en Île-de-France')

# Création et affichage de la carte
fig = px.scatter_mapbox(data_filtrée,
                        lat='Latitude',
                        lon='Longitude',
                        hover_name='ville',
                        hover_data={'Prix': True, 'Carburant': True, 'Latitude': False, 'Longitude': False},
                        color='Prix',  # Utilisation du prix pour la couleur des points
                        color_continuous_scale=px.colors.sequential.Viridis,  # Échelle de couleur pour les prix
                        zoom=9,
                        center={"lat": 48.8566, "lon": 2.3522},
                        title=f'Prix du {type_carburant_choisi} par Station',
                        mapbox_style="open-street-map")
st.plotly_chart(fig)

import streamlit as st
import pandas as pd
import plotly.express as px

# Charger et préparer les données
def load_data():
    data = pd.read_csv('prix-carburants.csv', sep=';')
    data[['Latitude', 'Longitude']] = data['geom'].str.split(',', expand=True)
    data['Latitude'] = pd.to_numeric(data['Latitude'], errors='coerce')
    data['Longitude'] = pd.to_numeric(data['Longitude'], errors='coerce')
    return data[data['Région'] == 'Île-de-France']

# Chargement des données
data = load_data()

# Filtrage des types de carburants spécifiques
types_carburant = ['Gazole', 'E10', 'SP98', 'SP95']
data = data[data['Carburant'].isin(types_carburant)]

# Calcul des prix moyens par type de carburant
prix_moyens = data.groupby('Carburant')['Prix'].mean().reset_index()

# Titre de la page
st.title('Analyse des Prix des Carburants en Île-de-France')

# Sélection du type de carburant pour la carte
type_carburant_choisi = st.selectbox('Choisir un type de carburant pour la carte:', types_carburant)
data_filtrée = data[data['Carburant'] == type_carburant_choisi]

# Affichage de la carte
fig_map = px.scatter_mapbox(data_filtrée,
                            lat='Latitude',
                            lon='Longitude',
                            hover_name='ville',
                            hover_data={'Prix': True, 'Carburant': True, 'Latitude': False, 'Longitude': False},
                            color='Prix',
                            color_continuous_scale=px.colors.sequential.Viridis,
                            zoom=9,
                            center={"lat": 48.8566, "lon": 2.3522},
                            title=f'Prix du {type_carburant_choisi} par Station',
                            mapbox_style="open-street-map")
st.plotly_chart(fig_map)

# Affichage du graphique à barres pour la comparaison des prix moyens
fig_bar = px.bar(prix_moyens, x='Carburant', y='Prix', title='Comparaison des Prix Moyens des Carburants')
st.plotly_chart(fig_bar)
