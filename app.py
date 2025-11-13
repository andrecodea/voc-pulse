# app.py (O Maestro)
import streamlit as st
import pandas as pd
from src.database.chroma_manager import initialize_chromadb
# --- MUDANÇA CRÍTICA ---
from src.chatbot.rag_chain import ManualRAGBot  # Importa nossa nova classe

# --- FIM DA MUDANÇA ---

# --- 1. Configuração da Página ---
st.set_page_config(
    page_title="VoC Pulse | Home",
    page_icon="🌡️",
    layout="wide"
)


# --- 2. Funções de Cache ---

@st.cache_data
def load_processed_data():
    try:
        df_enriched = pd.read_json("data/processed/data_enriched.json", lines=True)
        print("INFO: data_enriched.json carregado do cache.")
        return df_enriched
    except FileNotFoundError:
        st.error("ERRO CRÍTICO: 'data/processed/data_enriched.json' não encontrado.")
        st.error("Por favor, rode o script 'scripts/run_pipeline.py' primeiro!")
        st.stop()
    except Exception as e:
        st.error(f"Erro ao carregar data_enriched.json: {e}")
        st.stop()


@st.cache_resource
def load_chromadb_collection(_df_enriched):
    if _df_enriched is not None:
        print("INFO: Carregando ChromaDB...")
        collection = initialize_chromadb(_df_enriched)
        return collection
    return None


# --- MUDANÇA CRÍTICA ---
@st.cache_resource
def load_rag_bot(_chroma_collection):  # Renomeamos a função
    """
    Cria o nosso RAG Bot Manual.
    Roda apenas uma vez.
    """
    if _chroma_collection is not None:
        print("INFO: Carregando RAG Bot Manual...")
        rag_bot = ManualRAGBot(_chroma_collection)  # Cria nossa classe
        return rag_bot
    return None


# --- 3. Execução do Carregamento (O "Maestro") ---
with st.spinner("Carregando dados e inicializando IA..."):
    if 'data_loaded' not in st.session_state:
        print("INFO: Carregando dados pela primeira vez...")
        df_enriched = load_processed_data()
        chroma_collection = load_chromadb_collection(df_enriched)
        rag_bot = load_rag_bot(chroma_collection)  # Chama a nova função
        st.session_state.df_enriched = df_enriched
        st.session_state.chroma_collection = chroma_collection
        st.session_state.rag_bot = rag_bot  # Salva o bot na sessão
        st.session_state.data_loaded = True
        # --- FIM DA MUDANÇA ---

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