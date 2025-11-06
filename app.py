# app.py (O Maestro)
import streamlit as st
import pandas as pd
import sys
from src.database.chroma_manager import initialize_chromadb
from src.chatbot.rag_chain import create_rag_chain

# --- 1. Configuração da Página ---
# Define a configuração da página principal (Home)
st.set_page_config(
    page_title="VoC Pulse | Home",
    page_icon="🌡️",
    layout="wide"
)


# --- 2. Funções de Cache (O Coração do App) ---
# Estas funções rodam APENAS UMA VEZ e salvam seus resultados.

@st.cache_data  # Cache para dados (ex: DataFrames)
def load_processed_data():
    """
    Carrega os dados PRÉ-PROCESSADOS do JSON.
    Isso é rápido (instantâneo).
    """
    try:
        # Usamos 'lines=True' porque foi assim que o run_pipeline.py salvou
        df_enriched = pd.read_json("data/processed/data_enriched.json", lines=True)
        print("INFO: data_enriched.json carregado do cache.")
        return df_enriched
    except FileNotFoundError:
        st.error("ERRO CRÍTICO: 'data/processed/data_enriched.json' não encontrado.")
        st.error("Por favor, rode o script 'scripts/run_pipeline.py' primeiro!")
        st.stop()  # Para a execução do app
    except Exception as e:
        st.error(f"Erro ao carregar data_enriched.json: {e}")
        st.stop()


@st.cache_resource  # Cache para "recursos" (ex: conexões de DB, modelos de ML)
def load_chromadb_collection(_df_enriched):
    """
    Inicializa o ChromaDB EM MEMÓRIA com nossos dados.
    Roda apenas uma vez.
    """
    if _df_enriched is not None:
        print("INFO: Carregando ChromaDB...")
        collection = initialize_chromadb(_df_enriched)
        return collection
    return None


@st.cache_resource  # Cache para "recursos"
def load_rag_chain(_chroma_collection):
    """
    Cria a RAG Chain do LangChain.
    Roda apenas uma vez.
    """
    if _chroma_collection is not None:
        print("INFO: Carregando RAG Chain...")
        rag_chain = create_rag_chain(_chroma_collection)
        return rag_chain
    return None


# --- 3. Execução do Carregamento (O "Maestro") ---
# Este bloco 'if' é a chave. Ele só roda se os dados
# ainda não estiverem na memória da sessão.
if 'data_loaded' not in st.session_state:
    print("INFO: Carregando dados pela primeira vez...")

    # Chama as funções cacheadas
    df_enriched = load_processed_data()
    chroma_collection = load_chromadb_collection(df_enriched)
    rag_chain = load_rag_chain(chroma_collection)

    # Salva tudo no 'session_state' para as outras páginas usarem
    st.session_state.df_enriched = df_enriched
    st.session_state.chroma_collection = chroma_collection
    st.session_state.rag_chain = rag_chain
    st.session_state.data_loaded = True  # Marca que terminamos de carregar

    print("INFO: Dados e modelos carregados e salvos no session_state.")

# --- 4. Renderização da "Home Page" (app.py) ---
# Esta é a UI da página principal
st.title("🌡️ Bem-vindo ao VoC Pulse")
st.markdown("Um termômetro de performance 'Voice of Customer' com Embeddings.")
st.markdown("---")
st.subheader("Visão Geral do Projeto")
st.markdown(
    """
    Esta é a Prova de Conceito (POC) de uma aplicação que usa IA para analisar feedbacks de clientes.

    **Objetivo:** Transformar comentários (dados não estruturados) em insights acionáveis.

    **Como funciona:**
    1.  **Dashboard:** Analisa o sentimento e os tópicos dos feedbacks para criar gráficos de performance dos fornecedores.
    2.  **Chatbot:** Permite que você "converse" com seus dados de feedback usando um pipeline RAG (Geração Aumentada por Recuperação).
    """
)
st.markdown("#### Selecione uma página na barra lateral para começar:")
st.sidebar.success("Selecione uma página acima 👆")