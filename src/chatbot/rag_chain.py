# === CHATBOT ===
import streamlit as st
import yaml
import chromadb
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings

# 1. Importa configurações e prompts
try:
    with open("config/config.yaml", 'r') as f:
        config = yaml.safe_load(f)
    with open("config/prompts.yaml", 'r') as f:
        prompts = yaml.safe_load(f)

    RAG_PROMPT_TEMPLATE = prompts['rag_prompt_template']
    CHAT_MODEL = config['openai']['chat_model']
    EMBEDDING_MODEL = config['openai']['embedding_model']
    COLLECTION_NAME = config['chroma']['collection_name']
except FileNotFoundError as e:
    st.error(f"ERRO CRÍTICO: Arquivo de configuração não encontrado. {e}")
    st.stop()

# 2. Cria a chain de RAG
def create_rag_chain(chroma_collection: chromadb.Collection):
    """
    Creates and returns a LangChain RAG chain connected with a local
    ChromaDB vectorstore.
    :param chroma_collection:
    :return:
    """

    # 1. Configura LLM e Embeddings com a API da OpenAI
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        llm = ChatOpenAI(
        model_name = CHAT_MODEL,
        api_key=api_key,
        temperature=0.3
        )
        embedding_function = OpenAIEmbeddings(model=EMBEDDING_MODEL, api_key=api_key)
    except KeyError:
        st.error("ERRO: Chave 'OPENAI_API_KEY' não encontrada em .streamlit/secrets.toml.")
        st.stop()
    except Exception as e:
        st.error(f"ERRO ao inicializar LangChain: {e}")
        st.stop()

    # 2. Conectar o vectorstore com LangChain
    vectorstore = Chroma(
        client = chroma_collection._client,
        collection_name = chroma_collection.name,
        embedding_function=embedding_function
    )

    # 3. Busca os 5 melhores resultados
    retriever = vectorstore.as_retriever(search_kwargs={"k":5})

    # 4. Configura o PromptTemplate
    prompt = PromptTemplate(
        template = RAG_PROMPT_TEMPLATE,
        input_variables=["context", "question"]
    )

    # 5. Chain
    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff", # ENFIA o contexto no prompt
        retriever=retriever,
        chain_type_kwargs={"prompt":prompt},
        return_source_documents=True
    )
    print("INFO: Chain RAG criada com sucesso.")
    return rag_chain