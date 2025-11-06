# ===== PRÉ-PROCESSAMENTO DE DADOS PARA O APP STREAMLIT ====
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# 1. Habilita encontrar e importar módulos da pasta src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 2. Importa funções da pasta src/
from src.ingestion.data_loader import load_csv
from src.analysis.analyzer import run_ai_pipeline

# 3. Carrega as variáveis de ambiente presentes em .env ou .streamlit/secrets.toml
load_dotenv(".streamlit/secrets.toml")

# 4. Define os caminhos
INPUT_CSV_PATH = "data/raw/data.csv"
OUTPUT_JSON_PATH = "data/processed/data_enriched.json"

def main():
    print("--- INICIANDO PIPELINE DE PRÉ-PROCESSAMENTO ---")

    # 1. Pega a chave de API
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERRO CRÍTICO: OPENAI_API_KEY não encontrada.")
        print("Verifique se a chave está presente em .streamlit/secrets.toml")
        return

    # 2. Carrega os dados brutos
    df_raw= load_csv(INPUT_CSV_PATH)
    if df_raw.empty:
        print("Pipeline interrompido.")
        return

    # 3. Roda o motor de IA
    print(f"Iniciando análise de IA para {len(df_raw)} linhas...")
    df_enriched = run_ai_pipeline(df_raw, api_key)
    print("Análise de IA concluída.")

    # 4. Salva os resultados enriquecidos
    try:
        os.makedirs("data/processed", exist_ok=True)
        df_enriched.to_json(OUTPUT_JSON_PATH, orient='records', lines=True)
        print(f"SUCESSO! Dados enriquecidos salvos em: {OUTPUT_JSON_PATH}")
        print("\nVisualização das 5 primeiras linhas:")
        print(df_enriched.drop(columns=['embedding']).head())
    except Exception as e:
        print(f"ERRO ao salvar arquivo JSON: {e}")

if __name__ == "__main__":
    main()


