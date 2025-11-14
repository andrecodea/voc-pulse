# src/database/chroma_manager.py
import chromadb
import pandas as pd
import yaml

# 1. Carrega o nome da coleção via config.yaml
try:
    with open("config/config.yaml", 'r') as f:
        config = yaml.safe_load(f)
    COLLECTION_NAME = config['chroma']['collection_name']
except FileNotFoundError as e:
    print(f"ERRO: 'config/config.yaml' não encontrado. {e}")
    COLLECTION_NAME = "voc_pulse_default"


# 2. Inicializa o ChromaDB
def initialize_chromadb(df_enriched: pd.DataFrame):
    """
    Inicializa o ChromaDB em memória. Esta é a versão
    SIMPLES, sem nenhuma dependência do LangChain.
    """
    print("INFO: Inicializando ChromaDB em memória (modo simples)")
    client = chromadb.Client()

    # Simplesmente cria a coleção.
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    # 2. Remove as linhas em que a geração de embeddings falhou
    df_valid = df_enriched[df_enriched['embedding'].apply(lambda x: isinstance(x, list) and len(x) > 0)].copy()

    # 3. Imprime um aviso para cada linha descartada
    if len(df_valid) < len(df_enriched):
        print(f"INFO: {len(df_enriched) - len(df_valid)} linhas descartadas por falha no embedding.")

    # 4. Converte a coluna 'topico' (que pode ser uma lista) para string
    if 'topico' in df_valid.columns:
        df_valid['topico'] = df_valid['topico'].apply(
            lambda x: ', '.join(x) if isinstance(x, list) else x
        )

    # 5. Prepara metadados
    metadatas = df_valid.drop(columns=['Comentario_Cliente', 'embedding']).to_dict('records')

    # 6. Populando a coleção
    collection.add(
        embeddings=df_valid['embedding'].tolist(),
        documents=df_valid['Comentario_Cliente'].tolist(),
        metadatas=metadatas,
        ids=[str(i) for i in df_valid['ID_Evento']]
    )
    print(f"SUCESSO: {collection.count()} documentos carregados na coleção.")
    return collection
