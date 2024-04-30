import streamlit as st
import pandas as pd
from joblib import load
import numpy as np
from sklearn.metrics import r2_score

# Charger le modèle
model = load('knn_model.joblib')

# Configuration de la page
st.title('Prédictions de valeurs immobilières')
st.write('Cette application prédit les valeurs immobilières basées sur les entrées utilisateur.')

uploaded_file = st.file_uploader("Choisissez un fichier CSV pour évaluation", type='csv')
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    # Vérifier si les colonnes nécessaires sont présentes
    expected_columns = ['total_rooms', 'housing_median_age', 'median_income', 'total_bedrooms',
                        'ocean_proximity', 'population', 'households', 'latitude', 'longitude']
    if all(column in data.columns for column in expected_columns):
        X_new = data[expected_columns]

        # Faire la prédiction
        predictions = model.predict(X_new)

        # Calculer R²
        if 'median_house_value' in data.columns:
            y_true = data['median_house_value']
            score = r2_score(y_true, predictions)
            st.write(f'Le score R² pour les données fournies est: {score:.2f}')
        else:
            st.error("La colonne 'median_house_value' est nécessaire dans le CSV pour calculer le R².")
    else:
        st.error("Le fichier CSV doit contenir toutes les colonnes nécessaires: " + ", ".join(expected_columns))
else:
    st.write("Veuillez charger un fichier CSV pour évaluation.")

# Créer des inputs pour chaque caractéristique nécessaire
total_rooms = st.number_input('Total Rooms', min_value=0, max_value=10000, value=5000)
housing_median_age = st.number_input('Housing Median Age', min_value=0, max_value=100, value=35)
median_income = st.number_input('Median Income', min_value=0.0, max_value=20.0, value=3.0, step=0.1)
total_bedrooms = st.number_input('Total Bedrooms', min_value=1, max_value=10000, value=1000)
ocean_proximity = st.selectbox('Ocean Proximity', options=['<1H OCEAN', 'INLAND', 'NEAR OCEAN', 'NEAR BAY', 'ISLAND'])
population = st.number_input('Population', min_value=1, max_value=50000, value=3000)
households = st.number_input('Households', min_value=1, max_value=10000, value=500)

# Sliders pour la latitude et la longitude
latitude = st.slider('Latitude', min_value=32.0, max_value=42.0, value=34.05, format="%.4f")
longitude = st.slider('Longitude', min_value=-124.0, max_value=-114.0, value=-118.25, format="%.4f")

# Affichage de la carte qui se met à jour avec les sliders
map_data = pd.DataFrame({
    'lat': [latitude],
    'lon': [longitude]
})
st.map(map_data)

# Bouton pour faire des prédictions
if st.button('Prédire'):
    input_data = pd.DataFrame({
        'total_rooms': [total_rooms],
        'housing_median_age': [housing_median_age],
        'median_income': [median_income],
        'total_bedrooms': [total_bedrooms],
        'ocean_proximity': [ocean_proximity],
        'population': [population],
        'households': [households],
        'latitude': [latitude],
        'longitude': [longitude]
    })

    # Faire la prédiction en utilisant le modèle chargé
    prediction = model.predict(input_data)

    # Afficher la prédiction
    st.write(f'La valeur immobilière prédite est: ${prediction[0]:,.2f}')
