# === VISUALIZAÇÕES ===
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS

# 1. Distribuição de Sentimentos
def plot_sentiment_distribution(df_enriched: pd.DataFrame):
    """
    Generates a barplot for the general sentiment distribution.
    :param df_enriched:
    :return bar plot:
    """
    st.subheader("Distribuição Geral de Sentimentos")
    colors = {'Positivo': '#28a745', 'Negativo': '#dc3545', 'Misto': '#ffc107', 'Erro': '#6c757d'}
    sentiment_counts = df_enriched['sentimento'].value_counts()
    bar_colors = [colors.get(s, "#6c757d") for s in sentiment_counts.index]
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        x=sentiment_counts.index,
        y=sentiment_counts.values,
        pallete=bar_colors,
        ax=ax
    )

    ax.set_title("Contagem Total de Feedbacks por Sentimento", fontsize=16)
    ax.set_ylabel("Contagem")
    ax.set_ylabel("Sentimento")

    st.pyplot(fig)

def plot_semantic_pie_chart(df_enriched: pd.DataFrame):
    """
    Generates an interactive semantic pie plot.
    :param df_enriched
    """

    st.subheader("Análise Semântica por Fornecedor")
    colors = {'Positivo': '#28a745', 'Negativo': '#dc3545', 'Misto': '#ffc107', 'Erro': '#6c757d'}
    col1, col2 = st.columns(2)
    with col1:
        tipo_fornecedor = st.selectbox("Escolha a Categoria:", ["DJ", "Buffet"], key="pie_cat")

    if tipo_fornecedor == "DJ":
        col_name = "ID_Fornecedor_DJ"
    else:
        col_name = "ID_Fornecedor_Buffet"

    lista_fornecedores = df_enriched[col_name].unique()

    with col2:
        fornecedor_selecionado = st.selectbox(f"Selecione um {tipo_fornecedor}:",
                                              lista_fornecedores, key="pie_sup")

    if fornecedor_selecionado:
        df_filtrado = df_enriched[df_enriched[col_name] == fornecedor_selecionado]
        contagem_sentimentos = df_filtrado['sentimento'].value_counts()
        if not contagem_sentimentos.empty:
            pie_colors = [colors.get(s, '#6c757d') for s in contagem_sentimentos.index]
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.pie(
                contagem_sentimentos,
                labels=contagem_sentimentos.index,
                autopct='%1.1f%%',
                colors=pie_colors,
                startangle=90
            )
            ax.set_title(f"Distribuição de Sentimento para: {fornecedor_selecionado}")
            ax.axis('equal')
            st.pyplot(fig)
        else:
            st.warning(f"Não há dados de sentimento para {fornecedor_selecionado}")

custom_stopwords = set(STOPWORDS)
custom_stopwords.update([
"festa", "evento", "foi", "estava", "mas", "muito", "tudo", "como", "sobre",
    "dj", "buffet", "comida", "musica", "atendimento", "serviço", "sempre",
    "gostei", "achei", "bom", "ruim", "ótimo", "péssimo", "ok", "mas", "nao", "não",
    "muito", "pouco", "frio", "quente", "pista"
])

def plot_wordcloud_for_supplier(df_enriched: pd.DataFrame):
    """
    Generates an interactive WordCloud for a determined supplier
    :param df_enriched:
    :return:
    """
    st.subheader("Nuvem de Palavras (Word Cloud) por Fornecedor")

    # --- UI de Filtro (Copiada da Pizza, mas com chaves diferentes) ---
    col1, col2 = st.columns(2)
    with col1:
        tipo_fornecedor_wc = st.selectbox("Escolha a Categoria:",
                                          ["DJ", "Buffet"], key="wc_cat")

    if tipo_fornecedor_wc == "DJ":
        col_name_wc = "ID_Fornecedor_DJ"
    else:
        col_name_wc = "ID_Fornecedor_Buffet"

    lista_fornecedores_wc = df_enriched[col_name_wc].unique()

    with col2:
        fornecedor_selecionado_wc = st.selectbox(f"Selecione um {tipo_fornecedor_wc}:",
                                                 lista_fornecedores_wc, key="wc_sup")

    # --- Lógica de Geração do Word Cloud ---
    if fornecedor_selecionado_wc:
        # Filtra os comentários para o fornecedor
        df_filtrado_wc = df_enriched[df_enriched[col_name_wc] == fornecedor_selecionado_wc]

        # Junta todos os comentários em um único super-texto
        text = " ".join(comentario for comentario in df_filtrado_wc.Comentario_Cliente)

        if not text.strip():
            st.warning(f"Não há comentários em texto para {fornecedor_selecionado_wc}.")
        else:
            try:
                # Gera a nuvem de palavras
                wordcloud = WordCloud(
                    width=800,
                    height=400,
                    background_color='white',
                    stopwords=custom_stopwords,  # Usa nossa lista de stopwords
                    min_font_size=10
                ).generate(text)

                # Plota a nuvem no Streamlit
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.set_title(f"Palavras Mais Comuns para: {fornecedor_selecionado_wc}")
                ax.axis('off')
                st.pyplot(fig)

            except Exception as e:
                st.error(f"Erro ao gerar o Word Cloud: {e}")