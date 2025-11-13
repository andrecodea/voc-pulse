# pages/1_📊_Dashboard.py
import streamlit as st
import pandas as pd
from src.analysis.metrics import calculate_kpis
from src.visualization.charts import (
    plot_performance_over_time,
    plot_sentiment_distribution,
    plot_semantic_pie_chart,
    plot_wordcloud_for_supplier

)

# Configuração da página
st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
st.title("📊 Dashboard de Performance")

# --- 1. Guarda de Segurança ---
if 'data_loaded' not in st.session_state or st.session_state.df_enriched.empty:
    st.error("Os dados não foram carregados. Por favor, vá para a Home Page (app.py) primeiro.")
    st.stop()

# --- 2. Pega os Dados do Cache ---
df = st.session_state.df_enriched

# --- 3. Renderiza os KPIs (Como antes) ---
st.subheader("KPIs Gerais")
kpis = calculate_kpis(df)
col1, col2, col3 = st.columns(3)
col1.metric("Total de Feedbacks", kpis["total_feedbacks"])
col2.metric("Feedbacks Positivos", kpis["count_positivo"])
col3.metric("Taxa de Positividade", f"{kpis['pct_positivo']:.1f}%")

st.markdown("---")

plot_performance_over_time(df)

st.markdown("---")

# --- 4. LINHA 1: Gráficos de Análise (A SUA MUDANÇA) ---
# Cria as duas colunas
plot_sentiment_distribution(df)

st.markdown("---")

plot_semantic_pie_chart(df)

st.markdown("---")

# --- 5. LINHA 2: Word Cloud (Como você pediu, em 1 coluna) ---
plot_wordcloud_for_supplier(df)