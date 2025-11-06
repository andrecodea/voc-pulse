# pages/2_🤖_Chatbot.py
import streamlit as st

# Configuração da página
st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 Chatbot (RAG)")
st.markdown("Converse com seus dados de feedback em linguagem natural.")
st.markdown("---")

# --- 1. Guarda de Segurança (Verifica se o RAG está pronto) ---
if 'data_loaded' not in st.session_state:
    st.error("Os dados não foram carregados. Por favor, vá para a Home Page (app.py) primeiro.")
    st.stop()

# --- 2. Pega a Chain RAG do Cache ---
rag_chain = st.session_state.rag_chain

# --- 3. Lógica do Histórico do Chat ---
# Inicializa o histórico se ele não existir
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostra o histórico de mensagens (loop por todas as mensagens)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. Input do Usuário e Resposta do RAG ---
if user_query := st.chat_input("Ex: Quais os piores feedbacks do DJ C?"):

    # 4.1. Mostra a pergunta do usuário na tela
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # 4.2. Gera a resposta do RAG (IA)
    with st.spinner("Analisando feedbacks..."):
        try:
            # É AQUI que a "mágica" do RAG acontece
            response = rag_chain.invoke(user_query)
            resposta_ia = response['result']

            # (Opcional) Mostra as fontes que o RAG usou
            with st.expander("Ver fontes (documentos usados)"):
                st.write(response['source_documents'])

        except Exception as e:
            resposta_ia = f"Desculpe, ocorreu um erro ao processar sua pergunta: {e}"

    # 4.3. Mostra a resposta da IA na tela
    st.session_state.messages.append({"role": "assistant", "content": resposta_ia})
    with st.chat_message("assistant"):
        st.markdown(resposta_ia)

