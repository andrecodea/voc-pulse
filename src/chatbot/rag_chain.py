# src/chatbot/rag_chain.py
import streamlit as st
import yaml
import chromadb
from openai import OpenAI

# Carrega configs e prompts
try:
    with open("config/config.yaml", 'r') as f:
        config = yaml.safe_load(f)
    with open("config/prompts.yaml", 'r') as f:
        prompts = yaml.safe_load(f)

    RAG_PROMPT_TEMPLATE = prompts['rag_prompt_template']
    CHAT_MODEL = config['openai']['chat_model']
    EMBEDDING_MODEL = config['openai']['embedding_model']
except FileNotFoundError as e:
    st.error(f"ERRO CRÍTICO: Arquivo de configuração não encontrado. {e}")
    st.stop()


class ManualRAGBot:
    """
    Esta classe substitui o LangChain.
    Ela gerencia o RAG manualmente.
    """

    def __init__(self, collection: chromadb.Collection):
        try:
            self.api_key = st.secrets["OPENAI_API_KEY"]
            self.client = OpenAI(api_key=self.api_key)
            self.collection = collection
            print("INFO: RAGBot Manual inicializado com sucesso.")
        except KeyError:
            st.error("ERRO: Chave 'OPENAI_API_KEY' não encontrada.")
            st.stop()
        except Exception as e:
            st.error(f"ERRO ao inicializar o RAGBot: {e}")
            st.stop()

    def _get_relevant_documents(self, query: str) -> list[str]:
        """
        Passo 1: Gera embedding para a query e busca no ChromaDB.
        """
        try:
            # 1. Gera o embedding para a pergunta
            response = self.client.embeddings.create(
                model=EMBEDDING_MODEL,
                input=query
            )
            query_embedding = response.data[0].embedding

            # 2. Busca no ChromaDB usando o embedding
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=5,
                include=["documents"]
            )

            return results['documents'][0]  # Retorna a lista de textos

        except Exception as e:
            print(f"ERRO no Retrieval: {e}")
            return []

    def _generate_answer(self, query: str, context: list[str]) -> str:
        """
        Passo 2: Monta o prompt e chama o LLM da OpenAI.
        """
        # Junta os documentos em um único bloco de texto
        context_str = "\n\n".join(context)

        # Monta o prompt final
        final_prompt = RAG_PROMPT_TEMPLATE.format(
            context=context_str,
            question=query
        )

        try:
            # 3. Chama o Chat da OpenAI
            response = self.client.chat.completions.create(
                model=CHAT_MODEL,
                messages=[
                    {"role": "user", "content": final_prompt}
                ],
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"ERRO na Geração: {e}")
            return "Desculpe, ocorreu um erro ao gerar a resposta."

    def ask(self, query: str) -> str:
        """
        Função principal que executa o pipeline RAG.
        """
        # PASSO 1: RECUPERAÇÃO (Retrieval)
        relevant_documents = self._get_relevant_documents(query)

        if not relevant_documents:
            return "Desculpe, não encontrei nenhuma informação relevante sobre isso nos feedbacks."

        # PASSO 2: GERAÇÃO (Generation)
        answer = self._generate_answer(query, relevant_documents)
        return answer