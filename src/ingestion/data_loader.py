# ===== PIPELINE DE INGESTÃO DE DADOS =====
import pandas as pd
def load_csv(csv_path:str) -> pd.DataFrame:
    """Carrega o CSV bruto."""
    try:
        df = pd.read_csv(csv_path)
        print(f"INFO: CSV '{csv_path}' carregado. {len(df)} linhas.")
        return df
    except FileNotFoundError:
        print(f"ERRO: Arquivo '{csv_path}' não encontrado.")
        return pd.DataFrame()
