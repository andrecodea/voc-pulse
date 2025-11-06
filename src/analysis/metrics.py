# === CALCULO DE KPIs PARA DASHBOARDS ===
import pandas as pd

def calculate_kpis(df_enriched: pd.DataFrame) -> dict:
    """
    Computes the main KPIs from the enriched DataFrame and
    returns a dictionary containing the KPIs.
    :param df_enriched: Embedding enriched DataFrame.
    :return: dict object: KPI dictionary.
    """
    if df_enriched.empty:
        return {
            "total_feedbacks": 0,
            "count_positivo": 0,
            "count_negativo": 0,
            "count_misto": 0,
            "pct_positivo": 0
        }

    # Computa as contagens
    total_feedbacks = len(df_enriched)
    count_positivo = len(df_enriched[df_enriched['sentimento'] == 'Positivo'])
    count_negativo = len(df_enriched[df_enriched['sentimento'] == 'Negativo'])
    count_misto = len(df_enriched[df_enriched['sentimento'] == 'Misto'])

    # Computa o %
    if total_feedbacks > 0:
        pct_positivo = (count_positivo/total_feedbacks) * 100
    else:
        pct_positivo = 0

    # Retorna o dicionário final
    return {
        "total_feedbacks": total_feedbacks,
        "count_positivo": count_positivo,
        "count_negativo": count_negativo,
        "count_misto": count_misto,
        "pct_positivo": pct_positivo,
    }

