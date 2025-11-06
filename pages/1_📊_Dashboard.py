# pages/1_📊_Dashboard.py
import streamlit as st
import pandas as pd
from src.analysis.metrics import calculate_kpis # Importa nossa função de KPIs
from src.visualization.charts import (
    plot_sentiment_distribution,
    plot_semantic_pie_chart,
    plot_wordcloud_for_supplier
)

# Configuração da página
st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
st.title("📊 Dashboard de Performance")

# --- 1. Guarda de Segurança (Verifica se os dados estão prontos) ---
# Se o usuário abrir esta página direto, os dados não estarão prontos
if 'data_loaded' not in st.session_state:
    st.error("Os dados não foram carregados. Por favor, vá para a Home Page (app.py) primeiro.")
    st.stop() # Para a execução

# --- 2. Pega os Dados do Cache ---
# Pega o DataFrame que o app.py preparou
df = st.session_state.df_enriched

# --- 3. Renderiza os KPIs ---
st.subheader("KPIs Gerais")
# Chama nossa função de métricas
kpis = calculate_kpis(df)
col1, col2, col3 = st.columns(3)
col1.metric("Total de Feedbacks", kpis["total_feedbacks"])
col2.metric("Feedbacks Positivos", kpis["count_positivo"])
col3.metric("Taxa de Positividade", f"{kpis['pct_positivo']:.1f}%")

st.markdown("---")

# --- 4. Renderiza os Gráficos ---
# Chama as funções que criamos no charts.py
plot_sentiment_distribution(df)
st.markdown("---")
plot_semantic_pie_chart(df)
st.markdown("---")
plot_wordcloud_for_supplier(df)