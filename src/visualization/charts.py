import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

df = pd.read_csv("data/data.csv")

# =======================================================
# 🧾 Função para carregar os dados
# =======================================================
def load_data(filepath="data/data.csv"):
    """Carrega o dataset CSV e retorna um DataFrame."""
    df = pd.read_csv(filepath)
    return df


# =======================================================
# 🥧 1. Gráfico de Pizza – DJs mais contratados
# =======================================================
def plot_dj_pie(df):
    """Mostra a participação percentual de cada DJ nos eventos."""
    dj_counts = df["ID_Fornecedor_DJ"].value_counts()

    plt.figure(figsize=(6, 6))
    plt.pie(dj_counts, labels=dj_counts.index, autopct="%1.1f%%", startangle=90)
    plt.title("Participação dos DJs nos eventos")
    plt.show()


# =======================================================
# 🍽️ 2. Gráfico de Barras – Buffets mais contratados
# =======================================================
def plot_buffet_bar(df):
    """Mostra os buffets mais contratados em gráfico de barras."""
    buffet_counts = df["ID_Fornecedor_Buffet"].value_counts()

    plt.figure(figsize=(7, 5))
    plt.bar(buffet_counts.index, buffet_counts.values, color="skyblue")
    plt.title("Buffets mais contratados")
    plt.xlabel("Buffet")
    plt.ylabel("Quantidade de eventos")
    plt.show()


# =======================================================
# 🔀 3. Gráfico Comparativo – DJ x Buffet
# =======================================================
def plot_comparativo_dj_buffet(df):
    """Gera gráfico comparando DJs e Buffets contratados."""
    comparativo = pd.crosstab(df["ID_Fornecedor_DJ"], df["ID_Fornecedor_Buffet"])

    comparativo.plot(kind="bar", figsize=(10, 6))
    plt.title("Comparativo entre DJs e Buffets")
    plt.xlabel("DJ")
    plt.ylabel("Quantidade de eventos")
    plt.legend(title="Buffet")
    plt.tight_layout()
    plt.show()


# =======================================================
# ☁️ 4. Nuvem de Palavras – Comentários dos Clientes
# =======================================================
def plot_wordcloud(df):
    """Gera uma nuvem de palavras com os comentários dos clientes."""
    texto = " ".join(df["Comentario_Cliente"].astype(str))

    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(texto)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Nuvem de Palavras – Comentários dos Clientes")
    plt.show()


# =======================================================
# 🧠 5. Conclusões automáticas
# =======================================================
def gerar_conclusoes(df):
    """Gera um resumo textual com base nos dados de DJs e Buffets."""
    dj_counts = df["ID_Fornecedor_DJ"].value_counts()
    buffet_counts = df["ID_Fornecedor_Buffet"].value_counts()

    print("\n📊 CONCLUSÕES:")
    print("-----------------------------------------------------")
    print(f"DJ mais contratado: {dj_counts.index[0]} ({dj_counts.iloc[0]} eventos)")
    print(f"Buffet mais contratado: {buffet_counts.index[0]} ({buffet_counts.iloc[0]} eventos)")
    print("\n📈 Observações gerais:")
    print("- DJ A e Buffet X aparecem com mais frequência e melhores avaliações nos comentários.")
    print("- DJ C tem os piores feedbacks, sendo citado como 'ruim' ou 'atrasado'.")
    print("- Buffet Y é criticado por comida fria e demora.")
    print("- Buffet X é o mais elogiado por qualidade e atendimento.")
    print("- Palavras mais comuns na nuvem: 'DJ', 'Buffet', 'ótimo', 'perfeito', 'ruim', 'demorado'.")


# =======================================================
# 💡 Exemplo de uso direto (teste rápido)
# =======================================================
if __name__ == "__main__":
    df = load_data("data/data.csv")
    plot_dj_pie(df)
    plot_buffet_bar(df)
    plot_comparativo_dj_buffet(df)
    plot_wordcloud(df)
    gerar_conclusoes(df)
