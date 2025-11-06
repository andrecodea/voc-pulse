# pages/3_🗃️_Raw_Data.py
import streamlit as st

st.set_page_config(page_title="Dados", page_icon="🗃️", layout="wide")
st.title("🗃️ Dados Enriquecidos (Pós-Análise de IA)")

# --- Guarda de Segurança ---
if 'data_loaded' not in st.session_state:
    st.error("Os dados não foram carregados. Por favor, vá para a Home Page (app.py) primeiro.")
    st.stop()

# --- Pega os Dados do Cache ---
df = st.session_state.df_enriched

st.markdown("Estes são os dados que foram pré-processados pelo pipeline de IA.")
# Mostra o DataFrame (escondendo a coluna 'embedding' que é muito longa)
st.dataframe(df.drop(columns=['embedding']))