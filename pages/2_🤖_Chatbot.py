# pages/2_🤖_Chatbot.py
import streamlit as st

# Configuração da página
st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 Chatbot (RAG Manual)")
st.markdown("Converse com seus dados de feedback em linguagem natural.")
st.markdown("---")

# --- 1. Guarda de Segurança ---
if 'rag_bot' not in st.session_state:
    st.error("O Chatbot não foi inicializado. Por favor, vá para a Home Page (app.py) primeiro.")
    st.stop()

# --- 2. Pega o RAG Bot do Cache ---
# (Note a mudança de nome de 'rag_chain' para 'rag_bot')
rag_bot = st.session_state.rag_bot

# --- 3. Lógica do Histórico do Chat ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. Input do Usuário e Resposta do RAG ---
if user_query := st.chat_input("Ex: Quais os piores feedbacks do DJ C?"):

    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # 4.2. Gera a resposta do RAG (IA)
    with st.spinner("Analisando feedbacks..."):
        try:
            resposta_ia = rag_bot.ask(user_query)

        except Exception as e:
            resposta_ia = f"Desculpe, ocorreu um erro ao processar sua pergunta: {e}"

    # 4.3. Mostra a resposta da IA na tela
    st.session_state.messages.append({"role": "assistant", "content": resposta_ia})
    with st.chat_message("assistant"):
        st.markdown(resposta_ia)

