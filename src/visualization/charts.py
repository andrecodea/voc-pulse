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
        palette=bar_colors,
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


PALAVRAS_CHAVE_FILTRO = [
    # Positivas
    "bom", "ótimo", "excelente", "maravilhoso", "perfeito", "incrível", "sensacional",
    "gostei", "adorei", "amamos", "elogiaram", "elogio", "rápido", "atenciosos",
    "profissional", "impecável", "delicioso", "saboroso", "quente", "animado",
    "animou", "cheia", "legal", "top", "recomendo", "sucesso", "parabéns",

    # Negativas
    "ruim", "péssimo", "horrível", "desastre", "decepcionante", "chato", "fraco",
    "problema", "erro", "errou", "rude", "grossa", "atrasado", "atraso", "demorou",
    "frio", "fria", "morna", "vazia", "esquecível", "barulho", "repetitiva",
    "absurdo", "estressante", "gordurosa", "sumiu", "esqueceu", "faltou", "azedo",

    # Mistas / Neutras
    "ok", "mediano", "razoável", "normal"
]
# Transforma a lista em um Set (conjunto) para busca 1000x mais rápida
PALAVRAS_SET = set(PALAVRAS_CHAVE_FILTRO)


def plot_wordcloud_for_supplier(df_enriched: pd.DataFrame):
    """
    Cria um Word Cloud interativo com filtro de sentimento E
    usando a nossa Whitelist de palavras.
    """
    st.subheader("Nuvem de Palavras-Chave (Positivas/Negativas)")

    # 2. A UI de filtros (3 colunas, como antes)
    col1, col2, col3 = st.columns(3)

    with col1:
        tipo_fornecedor_wc = st.selectbox("Categoria:", ["DJ", "Buffet"], key="wc_cat")

    if tipo_fornecedor_wc == "DJ":
        col_name_wc = "ID_Fornecedor_DJ"
    else:
        col_name_wc = "ID_Fornecedor_Buffet"

    lista_fornecedores_wc = df_enriched[col_name_wc].unique()

    with col2:
        fornecedor_selecionado_wc = st.selectbox(f"Fornecedor:",
                                                 lista_fornecedores_wc, key="wc_sup")
    with col3:
        sentiment_filter = st.radio(
            "Filtrar Sentimento:",
            ["Todos", "Positivo", "Negativo", "Misto"],
            key="wc_sent",
            horizontal=True
        )

    # 3. Lógica de filtragem atualizada
    if fornecedor_selecionado_wc:

        # 3.1. Filtra pelo Fornecedor
        df_filtrado_wc = df_enriched[df_enriched[col_name_wc] == fornecedor_selecionado_wc]

        # 3.2. FILTRA PELO SENTIMENTO
        if sentiment_filter != "Todos":
            df_filtrado_wc = df_filtrado_wc[df_filtrado_wc['sentimento'] == sentiment_filter]

        # 3.3. Junta todos os comentários em um super-texto
        text = " ".join(comentario for comentario in df_filtrado_wc.Comentario_Cliente)

        # --- MUDANÇA CRÍTICA: LÓGICA DA WHITELIST ---

        # 3.4. Quebra o texto em palavras e filtra SÓ as que estão na nossa lista
        palavras_filtradas = []
        for palavra in text.lower().split():
            palavra_limpa = palavra.strip(".,!?:;()[]{}")  # Limpa pontuação
            if palavra_limpa in PALAVRAS_SET:
                palavras_filtradas.append(palavra_limpa)

        # 3.5. Junta as palavras filtradas de volta em um texto
        texto_filtrado = " ".join(palavras_filtradas)

        # ------------------------------------------------

        if not texto_filtrado.strip():
            st.warning(
                f"Nenhuma palavra-chave (bom, ruim, etc.) encontrada para '{sentiment_filter}' em {fornecedor_selecionado_wc}.")
        else:
            try:
                # 4. Gera a nuvem A PARTIR DO TEXTO FILTRADO
                wordcloud = WordCloud(
                    width=800,
                    height=400,
                    background_color='white',
                    # NÃO precisamos mais de 'stopwords', pois já filtramos!
                    collocations=False,  # Evita juntar palavras (ex: "muito bom")
                    min_font_size=10
                ).generate(texto_filtrado)  # <- Usa o texto novo

                # 5. Plota a nuvem
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.set_title(f"Palavras-Chave (Sent: {sentiment_filter}) para: {fornecedor_selecionado_wc}")
                ax.axis('off')
                st.pyplot(fig)

            except Exception as e:
                st.error(f"Erro ao gerar o Word Cloud: {e}")