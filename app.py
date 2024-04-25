import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='Ma Web App', layout='wide')

st.title('Bienvenue sur ma Web App avec Streamlit!')

st.write("Voici un exemple simple de graphique :")

data = pd.DataFrame(
    np.random.randn(50, 3),
    columns=['a', 'b', 'c']
)

st.line_chart(data)
