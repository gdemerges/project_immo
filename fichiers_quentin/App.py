import streamlit as st
import pandas as pd
import plotly.express as px

# Charger les données
@st.cache
def load_data():
    data = pd.read_csv("data/data4.csv")  # Charger votre dataset contenant les données GPS
    return data.copy()  # Cloner les données avant de les retourner

data = load_data()

# Set the background image
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://cdn.cnn.com/cnnnext/dam/assets/170606120957-california---travel-destination---shutterstock-220315747.jpg");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;
    background-repeat: no-repeat;
}
</style>
"""

st.markdown(background_image, unsafe_allow_html=True)


input_style = """
<style>
input[type="text"] {
    background-color: transparent;
    color: #a19eae;  // This changes the text color inside the input box
}
div[data-baseweb="base-input"] {
    background-color: transparent !important;
}
[data-testid="stAppViewContainer"] {
    background-color: transparent !important"""

#Afficher la carte interactive des points GPS avec tous les points
st.title('Carte interactive des points GPS')
fig = px.scatter_mapbox(data, lat="latitude", lon="longitude", zoom=5)
fig.update_layout(mapbox_style="open-street-map")
scatter_chart = st.plotly_chart(fig)

# Intro Modele Prediction
st.sidebar.title("Prédisez le prix de votre bien! ")

#Ajout des cases pour le modèle de prédiction:

select_total_rooms = st.sidebar.selectbox("Selectionner le nombres de pièces: ", options=range(1,21))
select_housing_median_age = st.sidebar.selectbox("Selectionner l'âge de la maison: ", options=range(1,53))
select_total_bedrooms = st.sidebar.selectbox("Selectionner le nombres de chambres: ", options=range(1,12))
select_ocean_proximity = st.sidebar.selectbox("Selectionner la proximité à la mer: ", options=['<1H OCEAN','INLAND','ISLAND','NEAR BAY','NEAR OCEAN'])
select_median_income = st.sidebar.text_input("Notez le revenu médian des ménages dans le quartier(de 1 à 15000): ")
select_latitude = st.sidebar.slider("Selectionnez une latitude",min_value=32.540000 ,max_value=41.950000 , value=34.260000)
select_longitude = st.sidebar.slider("Selectionnez une longitude",min_value=-124.350000 ,max_value=-114.310000 , value=-119.800000)

# Consulter les informations du point sélectionné
st.sidebar.title("Informations du point GPS sélectionné")

# Sélectionner le point sur la carte
selected_point_index = st.sidebar.selectbox("Sélectionner un point GPS", data.index)

# Afficher uniquement le point sélectionné sur la carte
selected_point_info = data.loc[selected_point_index]
selected_point_fig = px.scatter_mapbox(data, lat="latitude", lon="longitude", zoom=10)  # Utilisation de data au lieu de selected_point_info
selected_point_fig.update_traces(marker=dict(size=12, color="red"), selector=dict(mode='markers'))
selected_point_fig.update_layout(mapbox_style="open-street-map")
selected_point_chart = st.sidebar.plotly_chart(selected_point_fig)

# Afficher les informations du point sélectionné
for feature in data.columns:
    st.sidebar.write(f"{feature.capitalize()}: {selected_point_info[feature]}")

# Bouton de réinitialisation des filtres
if st.sidebar.button("Réinitialiser le filtre"):
    st.experimental_rerun()
