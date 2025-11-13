# === VISUALIZAÇÕES ===
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS

# --- MAPA DE CORES ---
COLOR_MAP = {'Positivo': '#28a745', 'Negativo':'#dc3545', 'Misto':'#ffc107', 'Erro':'#6c757d'}

# --- GRÁFICO DE PERFORMANCE SOBRE TEMPO ---
def plot_performance_over_time(df_enriched: pd.DataFrame):
    """
    Generates a plot of the supplier performance over time based on
    the historic mean .
    :param df_enriched:
    :return: line plot of supplier performance over time:
    """
    st.subheader("Tendência de Performance do Fornecedor (Plotly)")
    st.markdown("Veja como o sentimento dos clientes mudou ao longo do tempo.")

    # Mapeamento de Sentimentos
    score_map = {'Positivo': 1, "Misto": 0, "Negativo": -1}

    # Manipulação de Dados
    df = df_enriched.copy()
    df = df[df['sentimento'] != 'Erro'] # Ignora erros
    df['score_sentimento'] = df['sentimento'].map(score_map)
    df['Data_Evento'] = pd.to_datetime(df['Data_Evento'])

    # Seleção de Categoria de Fornecedor
    tipo_fornecedor = st.selectbox(
        "Escolha a Categoria de Fornecedor:",
        ['DJ', 'Buffet'],
        key="trend_cat"
    )

    if tipo_fornecedor == 'DJ':
        col_name = "ID_Fornecedor_DJ"
        titulo = "Performance Média de DJs ao Longo do Tempo"
    else:
        col_name = "ID_Fornecedor_Buffet"
        titulo = "Performance Média de Buffets ao Longo do Tempo"

    # Agrupamento de Dados
    df_trend = df.groupby([
        pd.Grouper(key='Data_Evento', freq='M'), # Agrupa por mês
        col_name
    ]).agg(score_medio=('score_sentimento', 'mean') # Calcula a média
          ).reset_index()

    if df_trend.empty:
        st.warning("Não há dados para plotar a tendência.")
        return

    # Cria e Plota o Gráfico
    fig = px.line(
        df_trend, x='Data_Evento', y='score_medio', color=col_name,
        title= titulo, markers=True,
        labels = {
            'score_medio': 'Score de Sentimento (de -1 a 1)',
            'Data_Evento': 'Mês', col_name: 'Fornecedor'
        }
    )

    fig.update_layout(hovermode='x unified') # Mostra os dados com o hover do mouse
    fig.update_yaxes(range=[-1.1, 1.1]) # Trava o eixo = Estabilidade
    st.plotly_chart(fig, use_container_width=True)

# --- GRÁFICO DE DISTRIBUIÇÃO GERAL ---
def plot_sentiment_distribution(df_enriched: pd.DataFrame):
    """Generates a general sentiment distribution barplot
    :param: df_enriched:
    :returns: Sentiment distribution barplot:
    """
    st.subheader("Distribuição Geral de Sentimentos por Fornecedor")

    # Define as cores das barras (com base nos sentimentos)
    colors = COLOR_MAP
    sentiment_counts = df_enriched['sentimento'].value_counts()
    bar_colors = [colors.get(s, '#6c757d') for s in sentiment_counts.index]

    # Cria a figura
    fig, ax = plt.subplots(figsize=(10, 5)) # fig = figura inteira, ax = eixo
    sns.barplot(
        x=sentiment_counts.index,
        y=sentiment_counts.values,
        palette=bar_colors,
        ax=ax
    )
    ax.set_title("Contagem Total de Feedbacks por Sentimento")
    ax.set_ylabel("Contagem")
    st.pyplot(fig)

# --- GRÁFICO DE DISTRIBUIÇÃO SEMÂNTICA INDIVIDUAL ---
def plot_semantic_pie_chart(df_enriched: pd.DataFrame):
    """
    Generates a semantic pie chart with sentiments for each supplier.
    :param df_enriched:
    :return Semantic pie plot:
    """
    st.subheader("Análise Semântica por Fornecedor")
    colors = COLOR_MAP

    # Interface de Filtragem
    col1, col2 = st.columns(2)

    # Coluna de Seleção de Categoria de Fornecedores
    with col1:
        tipo_fornecedor = st.selectbox(
            "Escolha a Categoria",
            ["DJ", "Buffet"],
            key='pie_cat') # Escolhe entre DJ e Buffet

    if tipo_fornecedor == "DJ": col_name = "ID_Fornecedor_DJ"
    else: col_name = "ID_Fornecedor_Buffet"

    lista_fornecedores = df_enriched[col_name].unique()

    #  Coluna de Seleção de Fornecedor Individual
    with col2:
        fornecedor_selecionado = st.selectbox(
            f"Selecione um {tipo_fornecedor}:",
            lista_fornecedores,
            key='pie_sup') # Escolhe entre fornecedores

    # Exibe o gráfico se houver um fornecedor selecionado
    if fornecedor_selecionado:
        df_filtrado = df_enriched[df_enriched[col_name] == fornecedor_selecionado]
        contagem_sentimentos = df_filtrado['sentimento'].value_counts()
        pie_colors = [colors.get(s, '#6c757d') for s in contagem_sentimentos.index]
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.pie(
            contagem_sentimentos,
            labels = contagem_sentimentos.index,
            autopct='%1.1f%%',
            colors=pie_colors,
            startangle=90
        )
        ax.set_title(f"Distribuição de Sentimento para: {fornecedor_selecionado}")
        ax.axis('equal')
        st.pyplot(fig)
    else:
        st.warning(f"Não há dados de sentimento para {fornecedor_selecionado}.")

# --- GRÁFICO DE NUVEM DE PALAVRAS ---
# Whitelist de Palavras-chave
PALAVRAS_CHAVE_FILTRO = [
    "bom", "ótimo", "excelente", "maravilhoso", "perfeito", "incrível", "sensacional",
    "gostei", "adorei", "amamos", "elogiaram", "elogio", "rápido", "atenciosos",
    "profissional", "impecável", "delicioso", "saboroso", "quente", "animado",
    "animou", "cheia", "legal", "top", "recomendo", "sucesso", "parabéns",
    "ruim", "péssimo", "horrível", "desastre", "decepcionante", "chato", "fraco",
    "problema", "erro", "errou", "rude", "grossa", "atrasado", "atraso", "demorou",
    "frio", "fria", "morna", "vazia", "esquecível", "barulho", "repetitiva",
    "absurdo", "estressante", "gordurosa", "sumiu", "esqueceu", "faltou", "azedo",
    "ok", "mediano", "razoável", "normal"
]
PALAVRAS_SET = set(PALAVRAS_CHAVE_FILTRO)

# Função de WordCloud
def plot_wordcloud_for_supplier(df_enriched: pd.DataFrame):
    """
    Generates a semantic wordcloud per supplier.
    :param df_enriched:
    :return Semantic Word Cloud:
    """
    st.subheader("Análise Semântica por Fornecedor")
    col1, col2, col3 = st.columns(3)

    with col1:
        tipo_fornecedor_wc = st.selectbox("Categoria:", ['DJ', 'Buffet'], key="wc_cat")
        if tipo_fornecedor_wc == "DJ":
            col_name_wc = "ID_Fornecedor_DJ"
        else:
            col_name_wc = "ID_Fornecedor_Buffet"

    lista_fornecedores_wc = df_enriched[col_name_wc].unique()

    with col2:
        fornecedor_selecionado_wc = st.selectbox(
            f"Fornecedor:",
            lista_fornecedores_wc,
            key='wc_sup'
        )
    with col3:
        sentiment_filter = st.radio(
            "Filtrar Sentimento:",
            ["Todos", "Positivo", "Negativo", "Misto"],
            key="wc_sent",
            horizontal=True
        )

    # Lógica de filtragem
    if fornecedor_selecionado_wc:
        # Filtra por fornecedor
        df_filtrado_wc = df_enriched[df_enriched[col_name_wc] == fornecedor_selecionado_wc]

        # Filtra por sentimento
        if sentiment_filter != "Todos":
            df_filtrado_wc = df_filtrado_wc[df_filtrado_wc['sentimento'] == sentiment_filter]

        # Enriquece o comentário
        text = " ".join(comentario for comentario in df_filtrado_wc.Comentario_Cliente)

        # Filtra com base na Whitelist
        palavras_filtradas = []
        for palavra in text.lower().split():
            palavra_limpa = palavra.strip(".,!?:;()[]{}") # Limpa pontuação
            if palavra_limpa in PALAVRAS_SET:
                palavras_filtradas.append(palavra_limpa)
        texto_filtrado = " ".join(palavras_filtradas)

        # Geração do Gráfico
        if not texto_filtrado.strip():
            st.warning(f"Nenhuma palavra-chave encontrada para '{sentiment_filter}' em {fornecedor_selecionado_wc}")
        else:
            try:
                wordcloud = WordCloud(
                    width=800,
                    height=400,
                    background_color='white',
                    collocations=False,
                    min_font_size=10
                ).generate(texto_filtrado) # Usa texto filtrado

                # Plotagem
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.set_title(f"Palavras-Chave (Sent: {sentiment_filter}) para {fornecedor_selecionado_wc}")
                ax.axis('off')
                st.pyplot(fig)
            except Exception as e:
                st.error(f"Erro ao gerar o Word Cloud: {e}")

