import pandas as pd
from openai import OpenAI
import json
import yaml
from concurrent.futures import ThreadPoolExecutor, as_completed

# ===== IMPORTA O PROMPT =====
try:
    with open("config/prompts.yaml", 'r') as f:
        prompts = yaml.safe_load(f)
        ANALYSIS_PROMPT = prompts['analysis_prompt']
except FileNotFoundError:
    print("ERRO: 'config/prompts.yaml' não encontrado.")
    ANALYSIS_PROMPT = ""

# ===== CRIA A CLASSE AI ANALYZER =====
class AIAnalyzer:
    """Encapsules the OpenAI AI analysis and embedding generation logics."""

    # Inicializa a classe
    def __init__(self, api_key:str):
        """
        Initializes the analyzer with the OpenAI API key and the OpenAI client.

        param: api_key (str): OpenAI API key
        """
        self.client = OpenAI(api_key=api_key)

    # Analisa e gera embeddings via API da OpenAI
    def get_analysis_and_embedding(self, text_review:str) -> dict:
        """
        Executes two API calls for one text_review:
        1. Sentiment and topic analysis via the ChatCompletion endpoint.
        2. Embedding generation.

        :param text_review:
        :return dictionary with three results: sentiment, topic, embedding:
        """
        analysis_result = {"sentimento": "Erro", "topico": "Erro"}
        embedding_result = []

        # --- 1. Chamada de Análise (Sentimento/Tópico) ---
        try:
            response_analysis = self.client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                response_format = {"type": "json_object"},
                messages = [
                    {"role": "system", "content": ANALYSIS_PROMPT},
                    {"role": "user", "content": text_review}
            ]
            )
            # Extrai o conteúdo JSON da resposta
            analysis_result = json.loads(response_analysis.choices[0].message.content)
        except Exception as e:
            # Imprime o erro sem parar a execução
            print(f"Erro na ANÁLISE para: {text_review[:30]}... | Erro: {e}")

        # --- 2. Chamada de Embedding ---
        try:
            response_embedding = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=text_review
            )
            embedding_result = response_embedding.data[0].embedding
        except Exception as e:
            print(f"Erro na GERAÇÃO DE EMBEDDING para: {text_review[:30]}... | Erro: {e}")

        # --- 3. Retorno Combinado ----
        return {
            "sentimento": analysis_result.get("sentimento", "Erro"),
            "topico": analysis_result.get("topico", "Erro"),
            "embedding": embedding_result
        }

# ===== CRIA O PIPELINE DE IA =====
def run_ai_pipeline(df: pd.DataFrame, api_key:str) -> pd.DataFrame:
    """
    Receives the raw DataFrame and enriches it by batches (paralLel).

    :param df:
    :param api_key:
    :return df_enriched:
    """
    #
    analyzer = AIAnalyzer(api_key=api_key)
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(analyzer.get_analysis_and_embedding, row): row for row in df['Comentario_Cliente']}
        temp_results = {}

        print(f"INFO: Iniciando {len(futures)} tarefas de análise da IA...")

        for future in as_completed(futures):
            original_comment = futures[future]
            try:
                result_dict = future.result()
                temp_results[original_comment] = result_dict
            except Exception as e:
                print(f"ERRO: Tarefa falhou completamente: {e}")
                temp_results[original_comment] = {"sentimento": "Falha", "topico": "Falha", "embedding":[]}

    print("INFO: Tarefas de IA concluídas. Montando DataFrame...")

    for comment in df['Comentario_Cliente']:
        results.append(temp_results.get(comment))

    df_results = pd.DataFrame(results)
    df_enriched = pd.concat([df.reset_index(drop=True), df_results], axis=1)

    return df_enriched